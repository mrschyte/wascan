import lxml.html
import itertools
import requests
import urllib.parse
import traceback
import argparse

from util.lists import *
from util.queue import *
from util.nhash import *
from util.urls import *

def find_links(tree, url):
    paths = ['//@href', '//@action', '//@src']

    for path in paths:
        for href in tree.xpath(path):
            if urllib.parse.urlparse(href).scheme == '':
                href = urllib.parse.urljoin(url, href)
            yield urlnorm(href)

class Scanner(object):
    def __init__(self, base=None):
        self.urls = UniqueQueue()
        self.urls.norm = urlnorm
        self.base = base

        self.session = requests.session()
        self.crawled = {}

    def on_request(self, url):
        pass

    def on_response(self, response, chash, unique):
        pass

    def add_crawled(self, chash, url):
        if chash not in self.crawled:
            self.crawled[chash] = set()

        self.crawled[chash].add(url)

    def was_crawled(self, chash):
        return chash in self.crawled

    def scan(self, url, wordlist=None):

        if self.base == None:
            self.base = url

        if wordlist == None:
            wordlist = []
        
        self.urls.put(url)

        while not self.urls.empty():
            
            try:
                url = self.urls.get()
                self.on_request(url)

                respn = self.session.get(url)
                chash = simhash(respn.content)

                if respn.ok:
                    self.on_response(response=respn, chash=chash, unique=(not self.was_crawled(chash)))
                    self.add_crawled(chash, respn.url)

                    ctype = respn.headers.get('content-type')
                    links = []

                    if 'html' in ctype or 'xml' in ctype:
                        xtree = lxml.html.fromstring(respn.text)
                        links = itertools.chain(links, find_links(xtree, url))

                    links = itertools.chain(links, urlprefixes(url))

                    for link in links:
                        if urlbase(self.base, link):
                            self.urls.put(link)

            except Exception as ex:
                traceback.print_exc()
                pass

        # do bruteforce passes
        m = len(wordlist)
        n = 0

        while m != n:
            m = len(self.crawled.values())
            for path in set(flatten(self.crawled.values())):
                for word in wordlist:
                    self.scan(urllib.parse.urljoin(path, word), [])
            n = len(self.crawled.values())
