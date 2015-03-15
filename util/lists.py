import unittest

def flatten(xs):
    if len(xs) == 0:
        return xs

    r = type(list(xs)[0])()

    for x in xs:
        if type(r) == set:
            r.update(x)
        elif type(r) == dict:
            r.update(x)
        elif type(r) == list:
            r.extend(x)
        else:
            raise TypeError

    return r

def trim(s, l, a):
    if len(s) > l:
        return (s[:l - len(a)] + a)[:l]
    return s

def head(xs):
    if type(xs) == list:
        if len(xs) > 0:
            return xs[0]
        return None
    else:
        return xs
    
class SelfTest(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(trim('abracadabra', 100, '...'), 'abracadabra')
        self.assertEqual(trim('abracadabra', 0, '...'), '')
        self.assertEqual(trim('abracadabra', 6, '...'), 'abr...')

    def test_flatten(self):
        self.assertEqual(flatten([[1],[2,3],[4,5,6]]), [1,2,3,4,5,6])
        self.assertEqual(flatten([set([1]),set([2,3]),set([4,5,6])]), set([1,2,3,4,5,6]))
        self.assertEqual(flatten([{1:1}, {2:2, 3:3}, {4:4, 5:5, 6:6}]), {1:1, 2:2, 3:3, 4:4, 5:5, 6:6})

    def test_head(self):
        self.assertEqual(head([1,2,3]), 1)
        self.assertEqual(head([]), None)
        self.assertEqual(head('alma'), 'alma')
        self.assertEqual(head(1), 1)

if __name__ == '__main__':
    unittest.main()
