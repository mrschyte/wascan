import lxml.html
import itertools
import requests
import urllib.parse
import threading
import sys
import traceback

from termcolor import colored

from util.files import *
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
    def __init__(self, base):
        self.urls = UniqueQueue()
        self.urls.norm = urlnorm
        self.base = base

        self.session = requests.session()
        self.crawled = {}

        self.urls.put(base)

    def on_request(self, url):
        sys.stderr.write('%s\r%s\r' % (' '*64, trim(url, 64, '...')))

    def on_response(self, response, chash, unique):

        if unique:
            color = 'green'
        else:
            color = 'yellow'
            
        print((colored('[%08x]', color) + ' %s') % (chash, response.url))

    def add_crawled(self, chash, url):
        if chash not in self.crawled:
            self.crawled[chash] = set()

        self.crawled[chash].add(url)

    def was_crawled(self, chash):
        return chash in self.crawled

    def scan(self, url=None, words=None):

        if url != None:
            self.urls.put(url)

        if words == None:
            words = []
        
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
                # traceback.print_exc()
                pass

        # do bruteforce passes
        m = len(wordlist)
        n = 0

        while m != n:
            m = len(self.crawled.values())
            for path in set(flatten(self.crawled.values())):
                for word in words:
                    self.scan(urllib.parse.urljoin(path, word), [])
            n = len(self.crawled.values())
        
wordlist = slurp('wordlists/directory-list-2.3-small.txt')
# wordlist = ['a','b','c','d','e','f']
s = Scanner(sys.argv[1])
s.scan(words=wordlist)
