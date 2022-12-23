from bs4 import BeautifulSoup
import requests
import pprint
import os
import json
import argparse

from bank_names import determine_bank_names

"""
TODO:
- √ fetch ID of central banks from speech list page: https://www.bis.org/dcms/api/token_data/institutions.json?list=cbspeeches&theme=cbspeeches&
- √extract name from central bank info
- √ subheading extraction
- √ store meta data in JSONL file
- √ Use hidden detail pages instead of direct links to PDF:
    - write it up as an email to BIS
- Deal with missing bank name matches: 
    (- When two bank names are found, return correct name or error message)
    - √ Names that are found in the JSON data are not mapped correctly (line 3730)
- √ make debug mode automatic/configurable
- for repeated websracping: force refetch of last cached list file instead of most recent list on website
- accept cache directory as argument
- use url-lib to parse bank-ID url
- convert PDFs into txt files
- evaluate pdftotxt --layout and similar options
- sanity check: do all list pages have 25 entries?
- add path of list page to each metadata (json) entry
"""

CACHE_FOLDER = 'cache'

def get_cache_path(path):
    return os.path.join(CACHE_FOLDER, path.lstrip('/'))


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

def extract_meta_data_from_speech_list_html(html_code, page):
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

        path = a_tag['href'].strip()
        speech_metadata = {
            'date': date_column.string.strip(),
            'title': a_tag.string.strip(),
            'detail_path': path if path.endswith('.htm') else None,
            'pdf_path': path if path.endswith('.pdf') else None,
            'page': page,
            'subheading': p_tag_text
        }
        
        speeches_metadata.append(speech_metadata)
    
    return speeches_metadata


def extract_pdf_path_from_speech_detail_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    a_tag = document.find('div', id='center').find('div', class_='pdftxt').find('a', class_='pdftitle_link')
    if a_tag is None:
        return None, None
    path = a_tag['href']

    relatedinfo_tag = document.find('div', id='center').find('div', id='relatedinfo-div')
    if relatedinfo_tag is None:
        return path, None

    a_tag_bank_id_link = relatedinfo_tag.find('a')
    parts = a_tag_bank_id_link['href'].split('institutions=')
    bank_ID = int(parts[1]) if len(parts) > 1 else None

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


def process_speech_lists(speeches_metadata, limit):
    html_code = fetch_list_page(1, True)
    page_count = extract_total_page_count_from_speech_list_html(html_code)

    current_page = 1
    while True:
        if limit is None or current_page == limit:
            html_code = fetch_list_page(current_page, current_page == page_count)
            speeches_metadata_of_current_page = extract_meta_data_from_speech_list_html(html_code, current_page)
            speeches_metadata.extend(speeches_metadata_of_current_page)

        if current_page >= page_count:
            break
        current_page += 1


def process_speech_detail_pages(speeches_metadata, errors, limit):
    for index, speech in enumerate(speeches_metadata):
        if limit is not None and limit not in speech['pdf_path'] and limit not in speech['detail_path']:
            continue

        print(index, speech['pdf_path'] or speech['detail_path'])
        if speech['pdf_path']:
            fetch_page_or_pdf(speech['pdf_path'])
        else:
            fetch_page_or_pdf(speech['detail_path'])
            html_code = read_file_from_cache(speech['detail_path'])
            pdf_path, bank_ID = extract_pdf_path_from_speech_detail_html(html_code)
            speech['pdf_path'] = pdf_path
            speech['bank_ID'] = bank_ID

            if pdf_path is None:
                errors.append('missing PDF link: ' + speech['detail_path'])
            else:
                fetch_page_or_pdf(pdf_path)


def main():
    parser = argparse.ArgumentParser(
                    prog = 'TODO: ProgramName',
                    description = 'TODO: What the program does',
                    epilog = 'TODO: Text at the bottom of help')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--limit-list', type=int)
    group.add_argument('--limit-detail')
    args = parser.parse_args()
    if args.limit_list:
        print(f'Only processing list page {args.limit_list}')
    if args.limit_detail:
        print(f'Only processing detail page {args.limit_detail}')
    

    speeches_metadata = []
    errors = []

    process_speech_lists(speeches_metadata, limit=args.limit_list)
    process_speech_detail_pages(speeches_metadata, errors, limit=args.limit_detail)
    determine_bank_names(speeches_metadata)
    
    with open('result.json', 'w') as f:
        json.dump(speeches_metadata, f, indent=4)
    print('Error: ', errors)

main()
# html_code = fetch_list_page(732, True)
# results = extract_meta_data_from_speech_list_html(html_code)
# pprint.pprint(results)