from bs4 import BeautifulSoup
import requests
import pprint


def fetch_speech_list(page):
    # We fetch pages in ascending order, starting with page 1 (= the oldest page). This way
    # the contents of a certain page remain the same; new speeches will be added to the page with
    # the hightest number. This allows to easily cache results in have the script fetch only pages
    # that have been appended since the last run.
    formdata = {
        'page': str(page),
        'paging_length': '25',
        'sort_list': 'date_asc',
        'theme': 'cbspeeches', # no idea what this is. The website sends this parameter, so we do as well.
        'objid': 'cbspeeches', # no idea what this is. The website sends this parameter, so we do as well.
    }

    response = requests.post('https://www.bis.org/doclist/cbspeeches.htm', data=formdata)

    # Note: The website responds with status 200 even for non-existing pages :-(
    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    html_code = response.text

    return html_code


def extract_total_page_count_from_speech_list_document(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    count_label = document.find('div', class_='pageof').find('span').string
    # How total page count is displayed on website: "1 of 1,827"
    count = count_label.split(' of ')[1].replace(',', '')
    return int(count)


def extract_info_from_speech_list_document(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    doc_list = document.find('table', class_='documentList')
    rows = doc_list.find_all('tr')

    speeches = []
    for row in rows:
        columns = row.find_all('td')
        date_column = columns[0]
        info_column = columns[1]

        a_tag = info_column.find('div', class_='title').find('a')

        speech_data = {
            'date': date_column.string.strip(),
            'title': a_tag.string.strip(),
            'path': a_tag['href'].strip(),
        }
        
        speeches.append(speech_data)
    
    return speeches


def main():
    speeches = []
    current_page = 1
    while True:
        print('Fetch page', current_page)
        html_code = fetch_speech_list(current_page)
        page_count = extract_total_page_count_from_speech_list_document(html_code)
        speeches.extend(extract_info_from_speech_list_document(html_code))
        if current_page > page_count or current_page > 10:
            break
        current_page += 1


    pprint.pprint(len(speeches))

main()