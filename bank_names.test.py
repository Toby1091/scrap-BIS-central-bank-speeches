import unittest

from bank_names import find_bank_names, map_bank_names

banks_from_json = {
    1: 'bank a', 
    2: 'bank b',
}
bank_name_mapping = {
    'bank b': 'Bank B',
    'bank c': 'Bank C',
    'bank d': 'Bank D',
}


class Test_find_bank_names(unittest.TestCase):
    def test_find_by_id(self):
        speech = {'bank_ID': 1}
        expected = ['bank a']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_in_banksFromJson_in_subheading(self):
        speech = {'subheading': 'xxx bank a yyy'}
        expected = ['bank a']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_multiple_in_banksFromJson_in_subheading(self):
        speech = {'subheading': 'xxx bank a yyy bank b zzz'}
        expected = ['bank a', 'bank b']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_in_bankNameMapping_in_subheading(self):
        speech = {'subheading': 'xxx bank c yyy'}
        expected = ['bank c']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_multiple_in_bankNameMapping_in_subheading(self):
        speech = {'subheading': 'xxx bank c yyy bank d zzz'}
        expected = ['bank c', 'bank d']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_multiple_in_banksFromJson_and_bankNameMapping_in_subheading(self):
        # the subheading contains 2 bank names; one is found in banksFromJson and one in bankNameMapping
        speech = {'subheading': 'xxx bank a yyy bank c zzz'}
        expected = ['bank a', 'bank c']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_nothing(self):
        speech = {'subheading': 'asdf'}
        expected = []
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)


class Test_map_bank_names(unittest.TestCase):
    def test(self):
        self.assertEqual(map_bank_names(['bank a', 'bank b'], bank_name_mapping), ['bank a', 'Bank B'])

if __name__ == '__main__':
    unittest.main()