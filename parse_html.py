from bs4 import BeautifulSoup

def extract_total_page_count_from_speech_list(html_code):
    document = BeautifulSoup(html_code, 'html.parser')
    count_label = document.find('div', class_='pageof').find('span').string
    # How total page count is displayed on website: "1 of 1,827"
    count = count_label.split(' of ')[1].replace(',', '')
    return int(count)

def extract_subheading_from_speech_list(p_tags):
    for p_tag in p_tags:
        strings = p_tag.strings
        for text in strings:
            stripped_text = text.strip()
            if stripped_text:
                return stripped_text

def extract_meta_data_from_speech_list(html_code, page):
    document = BeautifulSoup(html_code, 'html.parser')
    doc_list = document.find('table', class_='documentList')
    rows = doc_list.find_all('tr')

    speeches_metadata = []
    for row in rows:
        columns = row.find_all('td')
        date_column = columns[0]
        info_column = columns[1]
        p_tags = info_column.find_all('p')
        p_tag_text = extract_subheading_from_speech_list(p_tags)
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


def extract_pdf_path_from_speech_detail(html_code):
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
