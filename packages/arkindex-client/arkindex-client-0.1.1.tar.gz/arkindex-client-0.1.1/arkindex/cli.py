from arkindex import DEFAULT_HOST
from arkindex.conf import LocalConf
from arkindex.client import ArkindexAPI
import getpass
import uuid
import click

conf = LocalConf()


@click.group()
@click.option(
    '--profile',
    default='default',
    help='A reference name for your profile on this Arkindex host.',
)
@click.option(
    '--verify-ssl/--no-verify-ssl',
    default=True,
)
@click.pass_context
def main(context, profile, verify_ssl):
    context.ensure_object(dict)

    # Load existing profile from local configuration
    context.obj['profile_name'] = profile
    context.obj['profile'] = conf.profiles.get(profile)

    context.obj['verify_ssl'] = verify_ssl
    if not verify_ssl:
        # Warn once and disable urllib3's dozens of warnings
        click.echo('Will perform insecure HTTPS requests without checking SSL certificates.')
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@main.command()
@click.option(
    '--host',
    default=DEFAULT_HOST,
    prompt='Arkindex hostname',
    help='An Arkindex hostname to login.',
)
@click.option(
    '--email',
    prompt='Your email',
    help='Your account\'s email on this Arkindex host',
)
@click.pass_context
def login(context, host, email):
    '''
    Login on an arkindex host to get the credentials
    '''

    # Read password
    password = getpass.getpass(prompt='Your password: ')

    if context.obj.get('profile') and context.obj['profile'].get('token'):
        click.echo('You are about to overwrite existing credentials for "{}" in the "{}" profile.'.format(
            context.obj['profile']['email'], context.obj['profile_name']))
        click.confirm('Are you sure?', abort=True)

    # Try to login on the Arkindex server
    api = ArkindexAPI(host=host, verify_ssl=context.obj['verify_ssl'])
    try:
        resp = api.login(email, password)
    except Exception as e:
        click.echo('Login failed: {}'.format(e))
        return

    # Save token in local profile
    try:
        token = resp['auth_token']
    except KeyError:
        click.echo('Login successful, but the API did not return token info. Please contact a developer.')
        return
    if token is None:
        click.echo('Login successful, but no token is available. Please ask an admin.')
        return
    conf.save_profile(context.obj['profile_name'], host=host, email=email, token=token)
    conf.write()

    click.echo('Login successful !')


@main.command()
@click.argument(
    'corpus',
)
@click.argument(
    'files',
    nargs=-1,
    type=click.Path(exists=True),
)
@click.option(
    '--start/--no-start',
    help='Start a data import after a file is uploaded',
    default=True,
)
@click.option(
    '--mode',
    default='pdf',
    type=click.Choice(['pdf', 'images']),
    help='Data import type to start',
)
@click.option(
    '--volume',
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Output data import IDs',
)
@click.pass_context
def upload(context, files, corpus, start, mode, volume, verbose):
    '''
    Upload one or multiple files on the Arkindex host
    '''

    # Load the user profile
    profile = context.obj['profile']
    if profile is None:
        click.echo('Missing arkindex profile, please login first')
        return

    # Check auth
    # TODO: this should be automated once we have several commands
    try:
        api = ArkindexAPI(host=profile['host'], token=profile['token'], verify_ssl=context.obj['verify_ssl'])
        user = api.whoami()
        click.echo('Authentified as {} on {}'.format(user['email'], profile['host']))
    except Exception as e:
        click.echo('Authentification failed for profile {}: {}'.format(context.obj['profile_name'], e))
        return

    try:
        corpora = api.get_corpora()
    except Exception as e:
        click.echo('An error occured while fetching corpora: {}'.format(str(e)))
        return

    try:
        try:
            corpus_id = str(uuid.UUID(corpus))
            found_corpora = [c for c in corpora if c['id'] == corpus_id]
        except ValueError:
            found_corpora = [c for c in corpora if corpus.lower().strip() in c['name'].lower()]

        if len(found_corpora) == 0:
            click.echo('Corpus "{}" not found'.format(corpus))
            return
        elif len(found_corpora) > 1:
            click.echo('Multiple matching corpora for "{}". Please retry with a full name or ID'.format(corpus))
            click.echo('Matched corpora: "{}"'.format('", "'.join(c['name'] for c in found_corpora)))
            return

        corpus_id = found_corpora[0]['id']
    except Exception as e:
        click.echo('An error occured while matching corpora: {}'.format(str(e)))
        return

    volume_id = None

    if volume:
        try:
            volumes = list(api.get_elements(type='volume', corpus_id=corpus_id))
            try:
                volume_id = str(uuid.UUID(volume))
                found_volumes = [v for v in volumes if v['id'] == volume_id]
            except ValueError:  # Not a UUID
                found_volumes = [v for v in volumes if volume.lower().strip() in v['name'].lower()]

            if len(found_volumes) == 0:
                click.echo('Volume "{}" does not exist; it will be created'.format(volume))
            elif len(found_corpora) > 1:
                click.echo('Multiple matching volumes for "{}". Please retry with a full name or ID'.format(volume))
                click.echo('Matched volumes:')
                click.echo('\n'.join(v['name'] for v in found_volumes))
                return
            else:
                volume_id = found_volumes[0]['id']

        except Exception as e:
            click.echo('An error occured while matching volumes: {}'.format(str(e)))
            return

    file_ids, import_ids = [], []

    with click.progressbar(files, label='Uploading files') as bar:
        for local_file in bar:
            # Upload file
            try:
                datafile = api.upload_file(corpus_id, local_file)
                file_ids.append(datafile['id'])
            except Exception as e:
                click.echo('An error occured while uploading file {}: {}'.format(local_file, str(e)))
                continue

    if not start:
        click.echo('{} files uploaded'.format(len(file_ids)))
        return

    import_files = [file_ids, ]
    if not volume_id:
        # Put each file in its own import
        import_files = list(map(list, import_files))

    with click.progressbar(import_files, label='Starting imports') as bar:
        for file_list in import_files:
            # Start import
            try:
                dataimport = api.import_from_files(
                    mode,
                    file_list,
                    volume_id=volume_id,
                    # Send the volume name only if we are creating a new volume
                    volume_name=volume if not volume_id else None,
                )
                import_ids.append(dataimport['id'])
            except Exception as e:
                click.echo('An error occured while starting the import process for file {}: {}'.format(
                    local_file, str(e)))
                continue

    if not len(import_ids):
        click.echo('No imports started')
        return

    if verbose:
        click.echo('Started {} imports with IDs {}'.format(len(import_ids), ', '.join(import_ids)))
    else:
        click.echo('Started {} imports'.format(len(import_ids)))
