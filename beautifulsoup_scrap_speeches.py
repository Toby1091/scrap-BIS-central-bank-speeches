from bs4 import BeautifulSoup
import requests
import pprint



CACHE_FOLDER = 'cache'


def fetch_page_or_pdf(path):
    print('Fetch page', path)
    cache_path = os.path.join(CACHE_FOLDER, path.lstrip('/'))

    if os.path.exists(cache_path):
        return open(cache_path).read()

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

    return content


def extract_total_page_count_from_speech_list_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    count_label = document.find('div', class_='pageof').find('span').string
    # How total page count is displayed on website: "1 of 1,827"
    count = count_label.split(' of ')[1].replace(',', '')
    return int(count)


def extract_meta_data_from_speech_list_html(html_code):
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


def extract_pdf_path_from_speech_detail_html(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    a_tag = document.find('div', id='center').find('div', class_='pdftxt').find('a', class_='pdftitle_link')
    path = a_tag['href']
    return path


def main():
    speeches = []
    current_page = 1
    while True:
        # We fetch pages in ascending order, starting with page 1 (= the oldest page). This way
        # the contents of a certain page remain the same; new speeches will be added to the page with
        # the hightest number. This allows to easily cache results in have the script fetch only pages
        # that have been appended since the last run.
        params = f'?page={current_page}&paging_length=25&sort_list=date_desc'
        html_code = fetch_page_or_pdf('doclist/cbspeeches.htm' + params)

        page_count = extract_total_page_count_from_speech_list_html(html_code)
        speeches.extend(extract_meta_data_from_speech_list_html(html_code))
        if current_page > page_count or current_page > 10:
            break
        current_page += 1


    for speech in speeches:
        if speech['path'].endswith('.pdf'):
            fetch_page_or_pdf(speech['path'])
        else:
            html_code = fetch_page_or_pdf(speech['path'])
            pdf_path = extract_pdf_path_from_speech_detail_html(html_code)
            fetch_page_or_pdf(pdf_path)


    pprint.pprint(len(speeches))

main()