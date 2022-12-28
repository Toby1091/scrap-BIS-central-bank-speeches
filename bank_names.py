import requests
import json
import config
import argparse


def fetch_bank_list():
    response = requests.get('https://www.bis.org/dcms/api/token_data/institutions.json?list=cbspeeches&theme=cbspeeches&')
    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)
    banks_list = response.json()

    banks_dict = {}
    for d in banks_list:
        banks_dict[d['id']] = d['name']
    return banks_dict


def load_bank_name_mapping():
    """
    Reads bank name mapping file and returns a dict with 
        key=variant.lower()
        value=correct_  name
    """
    mapping = {}
    with open(config.BANK_NAMES_FILE) as f:
        for line_no, line in enumerate(f.readlines()):
            line = line.strip()
            try:                
                if line.startswith('#'):
                    continue
                correct_name, variants = line.split(': ')
                variants = variants.split(', ')
                for var in variants:
                    mapping[var.lower()] = correct_name
            except Exception as e:
                raise Exception(f'Error while reading list_of_missing_bank_names.txt in line {line_no + 1}:', e)
    return mapping


def find_bank_names(banks_from_json, bank_name_mapping, speech):
    """
    First search through all names in the JSON file retrieved from the website
    If a match is found return mapped name else return the found one.

    If no match is found, search through the variants in the manually defined mapping file.
    If a match is found return mapped name.
    """
    # Derive speech from Bank ID
    if speech.get('bank_ID') is not None:
        bank_name = banks_from_json[speech['bank_ID']]
        if bank_name.lower() in bank_name_mapping:
            bank_name =  bank_name_mapping[bank_name.lower()]
        return [bank_name]

    subheading = speech['subheading'].lower()
    
    # Search bank names from https://www.bis.org/.../institutions.json in subheading
    found_bank_names = []
    for bank_name in banks_from_json.values():
        if bank_name.lower() in subheading:
            if bank_name.lower() in bank_name_mapping:
                bank_name = bank_name_mapping[bank_name.lower()]
            found_bank_names.append(bank_name)
    if found_bank_names:
        return found_bank_names

    # Search bank names from list_of_missing_bank_names.txt in subheading
    found_bank_names = []
    for bank_name in bank_name_mapping:
        if bank_name in subheading:
            found_bank_names.append(bank_name_mapping[bank_name])
    return found_bank_names


def determine_bank_names(speeches_metadata):
    banks_from_json = fetch_bank_list()
    bank_name_mapping = load_bank_name_mapping()

    for speech in speeches_metadata:
        bank_names = find_bank_names(banks_from_json, bank_name_mapping, speech)

        if len(bank_names) > 1:
            # Looks like we've found a second bank name in the subheading.
            # We cannot know which one is the right one, so let's rather return None
            bank_name =  None
        elif len(bank_names) > 0:
            bank_name =  bank_names[0]
        else:
            bank_name = None

        speech['bank_name'] = bank_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Extends JSON with bank names derived from web and text file')
    parser.add_argument('input', help='JSON file to read from')
    parser.add_argument('output', help='JSON file to write to')
    args = parser.parse_args()

    resultJson = json.load(open(args.input))
    determine_bank_names(resultJson)
    json.dump(resultJson, open(args.output, 'w'), indent=4)