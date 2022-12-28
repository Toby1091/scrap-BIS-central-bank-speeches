import unittest

from bank_names import find_bank_names

banks_from_json = {
    1: 'bank a', 
    2: 'bank b',
}
bank_name_mapping = {
    'bank b': 'Bank B',
    'bank c': 'Bank C',
    'bank d': 'Bank D',
}


class TestFindBankNames(unittest.TestCase):
    def test_find_by_id(self):
        speech = {'bank_ID': 1}
        expected = ['bank a']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_by_id_with_mapping(self):
        speech = {'bank_ID': 2}
        expected = ['Bank B']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_in_banksFromJson_in_subheading(self):
        speech = {'subheading': 'xxx bank a yyy'}
        expected = ['bank a']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_in_banksFromJson_in_subheading_with_mapping(self):
        speech = {'subheading': 'xxx bank b yyy'}
        expected = ['Bank B']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_multiple_in_banksFromJson_in_subheading(self):
        speech = {'subheading': 'xxx bank a yyy bank b zzz'}
        expected = ['bank a', 'Bank B']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_in_bankNameMapping_in_subheading(self):
        speech = {'subheading': 'xxx bank c yyy'}
        expected = ['Bank C']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_multiple_in_bankNameMapping_in_subheading(self):
        speech = {'subheading': 'xxx bank c yyy bank d zzz'}
        expected = ['Bank C', 'Bank D']
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

    def test_find_nothing(self):
        speech = {'subheading': 'asdf'}
        expected = []
        self.assertEqual(find_bank_names(banks_from_json, bank_name_mapping, speech), expected)

if __name__ == '__main__':
    unittest.main()