from githubquery.GithubSession import GithubSession
import click
from termcolor import colored


def run():
    session = GithubSession(use_proxies=True)

    @click.command()
    @click.option(
        '--topic',
        required=True,
        help='Topic to search on, example "css"'
    )
    def search(topic):
        query = session.search(dict(
            p=1,
            q='topic:{}'.format(topic),
            type='Repositories'
        ))

        for result in query.results:
            print(colored(result.get('meta').get('full_name'), attrs=['bold']))
            print(result.get('meta').get('description'))
            print(colored(
                result.get('meta').get('ssh_url'), 'green', attrs=['underline']
            ))
            print('\n')

    search()
