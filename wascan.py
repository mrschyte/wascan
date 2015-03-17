import argparse
import scanner
import sys

from termcolor import colored

from util.files import slurp
from util.lists import trim

class Scanner(scanner.Scanner):
    def __init__(self, unique=False, brute=False, base=None):
        scanner.Scanner.__init__(self, base)
        self.unique = unique

    def on_request(self, url):
        sys.stderr.write('%s\r%s\r' % (' '*64, trim(url, 64, '...')))

    def on_response(self, response, chash, unique):
        if self.unique:
            if unique:
                print((colored('[%08x]', 'green') + ' %s') % (chash, response.url))
        else:
            if unique:
                color = 'green'
            else:
                color = 'yellow'

            print((colored('[%08x]', color) + ' %s') % (chash, response.url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Application Scanner')
    parser.add_argument('target', metavar='target', type=str, help='target url to scan')
    parser.add_argument('-u', '--unique', action='store_true', help='print only unique content')
    parser.add_argument('-b', '--brute', action='store_true', help='bruteforce urls')
    parser.add_argument('-w', metavar='path', help='set the wordlist to use', default='wordlists/directory-list-2.3-small.txt')

    args = parser.parse_args()
    s = Scanner(args.unique)

    if args.brute:
        wordlist = slurp(args.w)
    else:
        wordlist = None
    
    s.scan(url=args.target, wordlist=wordlist)

