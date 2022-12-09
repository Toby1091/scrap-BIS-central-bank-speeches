from bs4 import BeautifulSoup
import requests
import pprint



CACHE_FOLDER = 'cache'


def fetch_page(path):
    print('Fetch page', path)
    cache_path = os.path.join(CACHE_FOLDER, path.lstrip('/'))

    if os.path.exists(cache_path):
        return open(cache_path).read()

    response = requests.get('https://www.bis.org/' + path)

    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    html_code = response.text

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    file_handle = open(cache_path, 'w')
    file_handle.write(html_code)
    file_handle.close()

    return html_code


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


def fetch_pdf(path):
    print('Fetch pdf')
    response = requests.get('https://www.bis.org/' + path)

    if(response.status_code != 200):
        raise Exception('HTTP request failed with status code', response.status_code)

    filename = response.url.split('/')[-1]
    file_path = os.path.join('pdfs', filename)
    if os.path.exists(file_path):
        raise Exception('File %s exists already'.format(file_path))

    pdf = open(file_path, 'wb')
    pdf.write(response.content)
    pdf.close()


def main():
    speeches = []
    current_page = 1
    while True:
        # We fetch pages in ascending order, starting with page 1 (= the oldest page). This way
        # the contents of a certain page remain the same; new speeches will be added to the page with
        # the hightest number. This allows to easily cache results in have the script fetch only pages
        # that have been appended since the last run.
        params = f'?page={current_page}&paging_length=25&sort_list=date_desc'
        html_code = fetch_page('doclist/cbspeeches.htm' + params)

        page_count = extract_total_page_count_from_speech_list_html(html_code)
        speeches.extend(extract_meta_data_from_speech_list_html(html_code))
        if current_page > page_count or current_page > 10:
            break
        current_page += 1


    for speech in speeches:
        if speech['path'].endswith('.pdf'):
            fetch_pdf(speech['path'])
        else:
            html_code = fetch_page(speech['path'])
            pdf_path = extract_pdf_path_from_speech_detail_html(html_code)
            fetch_pdf(pdf_path)


    pprint.pprint(len(speeches))

main()