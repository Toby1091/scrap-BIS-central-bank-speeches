import csv
import json
import os

from slugify import slugify

import helpers

def export_as_one_csv():
    keywords = helpers.read_keywords_file()

    with open('output/keyword_by_bank.json', 'r') as file_handle:
        keywords_by_bank = json.load(file_handle)

    with open('output/keyword_by_speech_all.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['bank', 'speech count']
        headers.extend(keywords)
        writer.writerow(headers)

        sorted_bank_names = sorted(keywords_by_bank.keys())
        for bank_name in sorted_bank_names:
            bank_info = keywords_by_bank[bank_name]

            row = [
                bank_info['cb_name'], 
                bank_info['total_count_speeches']
            ]
            for keyword in keywords:    
                row.append(bank_info['keywords'].get(keyword, ''))

            writer.writerow(row)


def export_csv_per_bank():
    folder = os.path.join('output', 'csv_per_bank')
    os.makedirs(folder, exist_ok=True)

    with open('output/keyword_by_bank.json', 'r') as file_handle:
        keywords_by_bank = json.load(file_handle)

    sorted_bank_names = sorted(keywords_by_bank.keys())
    for bank_name in sorted_bank_names:
        bank_info = keywords_by_bank[bank_name]
        file_name = slugify(bank_info['cb_name'], separator='_',) + '.csv'
        with open(os.path.join(folder, file_name), 'w') as csvfile:
            writer = csv.writer(csvfile)
            headers = ['keyword', 'count']
            writer.writerow(headers)

            for keyword, count in bank_info['keywords'].items():
                writer.writerow([keyword, count])


def export_csv_per_keyword():
    folder = os.path.join('output', 'csv_per_keyword')
    os.makedirs(folder, exist_ok=True)

    keywords = helpers.read_keywords_file()

    with open('output/keyword_by_bank.json', 'r') as file_handle:
        keywords_by_bank = json.load(file_handle)

    for keyword in keywords:
        file_name = slugify(keyword.replace('*', '_star'), separator='_') + '.csv'
        with open(os.path.join(folder, file_name), 'w') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(['bank', 'count'])

            sorted_bank_names = sorted(keywords_by_bank.keys())
            for bank_name in sorted_bank_names:
                bank_info = keywords_by_bank[bank_name]
                if keyword in bank_info['keywords']:
                    writer.writerow([bank_info['cb_name'], bank_info['keywords'][keyword]])

export_as_one_csv()
export_csv_per_bank()
export_csv_per_keyword()



