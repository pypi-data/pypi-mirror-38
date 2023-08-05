import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_proxies():
    proxies = []
    headers = {'User-Agent': UserAgent().random}
    proxies_doc = requests.get('https://www.sslproxies.org/', headers=headers)
    soup = BeautifulSoup(proxies_doc.text, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'https': 'https://{}:{}'
            .format(row.find_all('td')[0].string, row.find_all('td')[1].string)
        })

    return proxies
