import unittest

from utils import reorder_found_strings

class Test_order_bank_names(unittest.TestCase):
    def test_1(self):
        self.assertEqual(reorder_found_strings({'c', 'a', 'b'}, 'a b c'), ['a', 'b', 'c'])

    def test_2(self):
        self.assertEqual(reorder_found_strings({'c', 'a', 'b'}, 'abc'), ['a', 'b', 'c'])


if __name__ == '__main__':
    unittest.main()