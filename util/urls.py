import unittest

import urllib.parse
import urltools

def urlnorm(url):
    u = urllib.parse.urlparse(urltools.normalize(url))
    path = u.path

    if len(path) > 0:
        if path[-1] == '/':
            path = path[:-1]

    v = (u.scheme, u.netloc, path, u.params, '', '')
    return urllib.parse.urlunparse(v)

def urlbase(base, url):
    u = urllib.parse.urlparse(urltools.normalize(base))
    v = urllib.parse.urlparse(urltools.normalize(url))

    return u.netloc == v.netloc and v.path.startswith(u.path)

def urlprefixes(url):
    parsed = urllib.parse.urlparse(url)
    chunks = parsed.path.split('/')[1:]

    for i in range(len(chunks)):
        yield '%s://%s/%s' % (parsed.scheme, parsed.netloc, '/'.join(chunks[:i]))

class SelfTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
