from bs4 import BeautifulSoup

import scrapy

# TODO:
# - validate output: verify that each page is present and has 25 entries (except the most recent one)


AMOUNT_OF_PAGES = 4#726

class Spider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.bis.org/cbspeeches/index.htm',
    ]

    def start_requests(self):
        for page in [700, 701]: #range(AMOUNT_OF_PAGES):
            formdata = {
                'page': str(page+1),
                'paging_length': '25',
                'sort_list': 'date_asc',
                'theme': 'cbspeeches',
                'objid': 'cbspeeches',
            }
            self.logger.info('page: %s', page + 1)
            yield scrapy.FormRequest(url='https://www.bis.org/doclist/cbspeeches.htm', formdata=formdata)
            page += 1

    def parse(self, response):
        page_num = response.css('.pageof span::text').get()
        for row in response.css('table tbody tr'):
            [date, speech_info] = row.css('td')
            speech_date = speech_info.css('.item_date td::text').get()
            title = speech_info.css('div.title a::text').get()
            url = speech_info.css('div.title a::attr("href")').get()

            yield {
                'title': title,
                'url': url,
                'page_num': int(page_num.split(' ')[0].replace(',', '')),
                'speech_date': speech_date
            }
tag = doc.title