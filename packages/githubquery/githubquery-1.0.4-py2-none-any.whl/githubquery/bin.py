from githubquery.GithubSession import GithubSession
from githubquery.exceptions import NotAuthorizedException
import click
from termcolor import colored


def list_repositories(results):
    for result in results:
        meta = result.get('meta')

        print(colored(meta.get('full_name'), attrs=['bold']))
        print(meta.get('description'))
        print(
            'language: {}'
            .format(colored(meta.get('language'), attrs=['underline']))
        )
        print(
            'stars: {}'
            .format(colored(meta.get('stargazers_count'), 'yellow'))
        )
        print(
            'updated: {}'.format(colored(meta.get('updated_at'), 'green')))
        print(colored(meta.get('ssh_url'), 'green', attrs=['underline']))
        print('\n')


def list_code(results):
    for result in results:
        print(result.get('filename'))
        print('\n')


def run():
    session = GithubSession(use_proxies=True)

    @click.command()
    @click.option(
        '--q',
        required=True,
        help='Topic to search on, example "css"'
    )
    @click.option(
        '--type',
        required=False,
        help='Type of query, example "repositories"'
    )
    def search(q, type='repositories'):
        try:
            query = session.search(dict(
                p=1,
                q=q,
                type=type
            ))
        except NotAuthorizedException as e:
            print(colored(e.message, 'red'))
            return False

        if type == 'repositories':
            list_repositories(query.results)
        elif type == 'code':
            list_code(query.results)

    search()
