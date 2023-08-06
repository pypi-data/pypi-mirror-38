import requests
from bs4 import BeautifulSoup
from urlparse import urljoin


def get_document(url):
    print(url)
    try:
        document = BeautifulSoup(requests.get(url).text, 'html.parser')
    except Exception:
        return None

    setattr(document, 'url', url)
    return document


def get_urls(document):
    return list(
        set(
            [
                urljoin(document.url, a.get('href'))
                for a in document.find_all('a')
            ]
        )
    )


def scrape(urls, selector, limit, visited_urls=[], found=[]):
    new_urls = []

    for url in urls:
        document = get_document(url)

        if not document:
            continue

        found = found + document.select(selector)
        new_urls = new_urls + get_urls(document)

        print(len(found))

        if len(found) >= limit:
            return found

    return scrape(list(set(new_urls)), selector, limit, visited_urls, found)
