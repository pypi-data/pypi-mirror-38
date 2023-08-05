import requests
import urllib
from urlparse import urljoin
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from githubquery.exceptions import (
    MissingArgumentException,
    TooManyRequestsException
)
from githubquery.QueryIterator import QueryIterator
from githubquery.proxies import get_proxies
import random


class GithubSession(object):

    def __init__(self):
        self.headers = {
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  # noqa E501
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-US;q=0.6',  # noqa E501
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'github.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.base_url = 'https://github.com'
        self.search_url = '/search'
        self.proxies = get_proxies()
        self.obtain_new_proxy()

    def obtain_new_proxy(self):
        self.proxy = self.proxies[random.randint(0, len(self.proxies) - 1)]

    def search(self, arguments):
        return QueryIterator(
            self,
            arguments,
            self.search_handler(arguments)
        )

    def search_handler(self, arguments):
        if 'type' not in arguments:
            raise MissingArgumentException('Missing argument: `type`')

        arguments['ref'] = 'advsearch'
        arguments['utf8'] = 1

        query_params = '?' + urllib.urlencode(arguments, doseq=True)
        url = urljoin(self.base_url, self.search_url) + query_params
        resp = self.session.get(url, proxies=self.proxy)

        if resp.status_code == 429:
            raise TooManyRequestsException('Too many requests')

        soup = BeautifulSoup(resp.text, 'html.parser')

        if arguments.get('type').lower() == 'repositories':
            return self.search_repositories(soup)

    def search_repositories(self, soup):
        return [
            dict(
                title=item.select_one('h3 a').text,
                url=urljoin(
                    self.base_url,
                    item.select_one('h3 a').get('href')
                )
            )
            for item in soup.select('.repo-list-item')
        ]
