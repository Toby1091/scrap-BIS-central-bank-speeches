from bs4 import BeautifulSoup
import requests
import pprint
import os

"""
TODO:
- √ fetch ID of central banks from speech list page: https://www.bis.org/dcms/api/token_data/institutions.json?list=cbspeeches&theme=cbspeeches&
- for repeated websracping: force refetch of last cached list file instead of most recent list on website
- extract name from central bank info
- √ subheading extraction
- Deal with missing bank name matches
- store meta data in JSONL file
- make debug mode automatic/configurable
- accept cache directory as argument
- use url-lib to parse bank-ID url
- resolve bank-ID into bank name
- convert PDFs into txt files
"""


CACHE_FOLDER = 'cache'

def get_cache_path(path):
    return os.path.join(CACHE_FOLDER, path.lstrip('/'))


def fetch_bank_list():
    response = requests.get('https://www.bis.org/dcms/api/token_data/institutions.json?list=cbspeeches&theme=cbspeeches&')
    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)
    banks_list = response.json()

    banks_dict = {}
    for d in banks_list:
        banks_dict[d['id']] = d['name']
    return banks_dict


def find_bank_name(banks_dict, subheading):
    for bank_name in banks_dict.values():
        if bank_name.lower() in subheading.lower():
            return bank_name


def fetch_page_or_pdf(path, force_refetch=False):
    print(f'Fetch page {path} (force refetch={force_refetch})')
    cache_path = get_cache_path(path)

    if not force_refetch and os.path.exists(cache_path):
        return

    response = requests.get('https://www.bis.org/' + path)

    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    is_pdf = response.headers['content-type'].lower().startswith('application/pdf')
    mode = 'wb' if is_pdf else 'w'
    content = response.content if is_pdf else response.text

    file_handle = open(cache_path, mode)
    file_handle.write(content)
    file_handle.close()


def read_file_from_cache(path):
    cache_path = get_cache_path(path)
    return open(cache_path).read()


def extract_total_page_count_from_speech_list_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    count_label = document.find('div', class_='pageof').find('span').string
    # How total page count is displayed on website: "1 of 1,827"
    count = count_label.split(' of ')[1].replace(',', '')
    return int(count)

def extract_subheading_from_speech_list_html(p_tags):
    for p_tag in p_tags:
        strings = p_tag.strings
        for text in strings:
            stripped_text = text.strip()
            if stripped_text:
                return stripped_text

def extract_meta_data_from_speech_list_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    doc_list = document.find('table', class_='documentList')
    rows = doc_list.find_all('tr')

    speeches_metadata = []
    for row in rows:
        columns = row.find_all('td')
        date_column = columns[0]
        info_column = columns[1]
        p_tags = info_column.find_all('p')
        p_tag_text = extract_subheading_from_speech_list_html(p_tags)
        a_tag = info_column.find('div', class_='title').find('a')

        speech_metadata = {
            'date': date_column.string.strip(),
            'title': a_tag.string.strip(),
            'path': a_tag['href'].strip(),
            'subheading': p_tag_text
        }
        
        speeches_metadata.append(speech_metadata)
    
    return speeches_metadata


def extract_pdf_path_from_speech_detail_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    a_tag = document.find('div', id='center').find('div', class_='pdftxt').find('a', class_='pdftitle_link')
    if a_tag is None:
        return None, None

    relatedinfo_tag = document.find('div', id='center').find('div', id='relatedinfo-div')
    if relatedinfo_tag is None:
        return None, None

    a_tag_bank_id_link = relatedinfo_tag.find('a')

    parts = a_tag_bank_id_link['href'].split('institutions=')
    bank_ID = int(parts[1]) if len(parts) > 1 else None
    path = a_tag['href']

    return path, bank_ID


def fetch_list_page(page_number, force_refetch):
    # We fetch pages in ascending order, starting with page 1 (= the oldest page). This way
    # the contents of a certain page remain the same; new speeches_metadata will be added to the page with
    # the hightest number. This allows to easily cache results in have the script fetch only pages
    # that have been appended since the last run.
    params = f'?page={page_number}&paging_length=25&sort_list=date_asc'
    path = 'doclist/cbspeeches.htm' + params

    fetch_page_or_pdf(path, force_refetch)
    html_code = read_file_from_cache(path)
    return html_code


def process_speech_lists(speeches_metadata):
    html_code = fetch_list_page(1, True)
    page_count = extract_total_page_count_from_speech_list_html(html_code)

    current_page = 1
    while True:
        html_code = fetch_list_page(current_page, current_page == page_count)
        speeches_metadata_of_current_page = extract_meta_data_from_speech_list_html(html_code)
        speeches_metadata.extend(speeches_metadata_of_current_page)
        if current_page >= page_count or current_page > 1:
            break
        current_page += 1


def process_speech_detail_pages(speeches_metadata, errors):
    banks_dict = fetch_bank_list()

    for index, speech in enumerate(speeches_metadata):
        print(index)
        if speech['path'].endswith('.pdf'):
            fetch_page_or_pdf(speech['path'])
            speech['central_bank'] = find_bank_name(banks_dict, speech['subheading'])
        else:
            fetch_page_or_pdf(speech['path'])
            html_code = read_file_from_cache(speech['path'])
            path, bank_ID = extract_pdf_path_from_speech_detail_html(html_code)

            if bank_ID is None:
                bank_ID = find_bank_name(banks_dict, speech['subheading'])

            if path is None:
                errors.append('missing PDF link: ' + speech['path'])
            else:
                fetch_page_or_pdf(path)
                bank_name = banks_dict.get(bank_ID)
                speech['central_bank'] = bank_name


def main():
    speeches_metadata = []
    errors = []

    process_speech_lists(speeches_metadata)
    process_speech_detail_pages(speeches_metadata, errors)
    
    pprint.pprint(speeches_metadata)
    print('Error: ', errors)

main()
# html_code = fetch_list_page(732, True)
# results = extract_meta_data_from_speech_list_html(html_code)
# pprint.pprint(results)