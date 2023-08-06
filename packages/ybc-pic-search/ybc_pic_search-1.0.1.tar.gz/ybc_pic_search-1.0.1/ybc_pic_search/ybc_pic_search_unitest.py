import unittest
from .ybc_pic_search import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(0, pic_search('彭于晏'))


if __name__ == '__main__':
    unittest.main()
