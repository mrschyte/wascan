import unittest

def identity(x):
    return x


class SelfTest(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(3, identity(3))
        self.assertEqual(set(), identity(set()))
        self.assertEqual('hello', identity('hello'))

if __name__ == '__main__':
    unittest.main()
