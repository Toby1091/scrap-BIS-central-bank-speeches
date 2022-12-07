from bs4 import BeautifulSoup
import requests
import pprint


def fetch_speech_list():
    # page = 1
    formdata = {
        #'page': str(page),
        #'paging_length': '25',
        #'sort_list': 'date_asc',
        'theme': 'cbspeeches',
        'objid': 'cbspeeches',
    }

    response = requests.post('https://www.bis.org/doclist/cbspeeches.htm', data=formdata)

    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    html_code = response.text

    return html_code


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


html_code = fetch_speech_list()
speeches = extract_info_from_speech_list_document(html_code)
pprint.pprint(speeches)
