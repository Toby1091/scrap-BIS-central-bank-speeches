import json
import argparse

from bank_names import determine_bank_names
import parse_html
from cache import fetch_page_or_pdf, read_file_from_cache
import config

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


def fetch_list_page(page_number, force_refetch):
    # We fetch pages in ascending order, starting with page 1 (= the oldest page). This way
    # the contents of a certain page remain the same; new speeches_metadata will be added to the page with
    # the hightest number. This allows to easily cache results in have the script fetch only pages
    # that have been appended since the last run.
    params = f'?page={page_number}&paging_length={config.PAGE_SIZE}&sort_list=date_asc'
    path = 'doclist/cbspeeches.htm' + params

    fetch_page_or_pdf(path, force_refetch)
    html_code = read_file_from_cache(path)
    return html_code


def process_speech_lists(speeches_metadata, limit):
    html_code = fetch_list_page(1, True)
    page_count = parse_html.extract_total_page_count_from_speech_list(html_code)

    current_page = 1
    while True:
        if limit is None or current_page == limit:
            html_code = fetch_list_page(current_page, current_page == page_count)
            speeches_metadata_of_current_page = parse_html.extract_meta_data_from_speech_list(html_code, current_page)
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
            pdf_path, bank_ID = parse_html.extract_pdf_path_from_speech_detail(html_code)
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
    
    with open(config.RESULT_FILE, 'w') as f:
        json.dump(speeches_metadata, f, indent=4)
    print('Error: ', errors)

main()
# html_code = fetch_list_page(732, True)
# results = extract_meta_data_from_speech_list_html(html_code)
# pprint.pprint(results)