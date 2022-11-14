import scrapy

# TODO:
# - write current page number to file
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
        for row in response.css('table tbody tr'):
            [date, speech_info] = row.css('td')
            title = speech_info.css('div.title a::text').get()
            url = speech_info.css('div.title a::attr("href")').get()

            yield {
                'title': speech_info.css('div.title a::text').get(),
                'url': speech_info.css('div.title a::attr("href")').get(),
            }
