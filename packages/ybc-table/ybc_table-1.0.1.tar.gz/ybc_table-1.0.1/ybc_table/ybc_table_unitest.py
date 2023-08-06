import unittest
from ybc_table import *


class MyTestCase(unittest.TestCase):
    def test_table(self):
        s = '+---+---+---+\n| 1 | 2 | 3 |\n+---+---+---+\n| 4 | 5 | 6 |\n+---+---+---+'
        l = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(s, table(l))


if __name__ == '__main__':
    unittest.main()
