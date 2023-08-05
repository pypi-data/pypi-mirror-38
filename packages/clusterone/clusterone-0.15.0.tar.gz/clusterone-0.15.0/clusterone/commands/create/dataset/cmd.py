import time

import click

from clusterone import authenticate
from clusterone import client
from clusterone.business_logic.dataset_commands import CreateGCSDatasetCommand
from clusterone.business_logic.providers import Providers
from clusterone.client_exceptions import RemoteAquisitionFailure
from clusterone.messages import dataset_creation_in_progress_message


def aquire_remote(name, session, client):
    username = session.get('username')
    retry_count, retry_interval = session.retry_count, session.retry_interval

    for _ in range(retry_count):
        time.sleep(retry_interval)

        dataset = client.get_dataset(name, username)
        git_url = dataset['git_auth_link']

        # API response might be evaluated as None or ""
        if not (git_url is None or git_url == ""):
            return git_url

    raise RemoteAquisitionFailure()


@click.command()
@click.pass_obj
@authenticate()
@click.argument('source', default='gitlab')
@click.argument('name', required=False)
@click.option('--description', default='')
def command(context, name, source, description):
    """
    Create a new Clusterone dataset and output its remote URL
    """
    if source == Providers.GCS:
        create_command = CreateGCSDatasetCommand(context.client, name)
        result = create_command.execute()

        if result['errors']:
            click.echo(result['errors'])

        click.echo(result['output'])
        return

    session = context.session

    # handling default case - this should not work like that
    if not any(map(lambda choice: source in choice, ['s3', 'github', 'gitlab'])):
        name = source
        source = 'gitlab'

    if source == 'github':
        raise NotImplemented()

    click.echo(dataset_creation_in_progress_message)

    dataset = client.create_dataset(name, source, description)
    dataset_name = dataset['name']

    if dataset.get('source') == 'gitlab':
        remote_url = dataset.get('git_auth_link')
        # Refactor
        if not remote_url:
            # Try to get remote URL for gitlab
            remote_url = aquire_remote(dataset_name, client=client, session=session)
    else:
        # Handle Github and S3
        remote_url = dataset.get('http_url_to_repo')

    click.echo(remote_url)

    # Warning! This is untested!
    session['current_dataset'], session['current_dataset_name'] = [dataset_name] * 2
    session.save()

    return remote_url
