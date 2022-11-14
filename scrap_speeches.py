import json
import scrapy
import os

speech_list = [json.loads(row) for row in open('speeches.jsonl').readlines()]

class Spider(scrapy.Spider):
    name = 'speeches'
    start_urls = ['https://www.bis.org/' + entry['url'] for entry in speech_list]

    def parse(self, response):
        id = response.url.split('/')[-1].split('.')[0]
        if response.headers['content-type'].startswith(b'application/pdf'):
            file_path = 'pdfs/' + id + '.pdf'
            if os.path.exists(file_path):
                raise Exception('File %s exists already'.format(file_path))
            pdf = open('pdfs/' + id + '.pdf', 'wb')
            pdf.write(response.body)
        else:
            pdf_url = response.css('div.pdftitle a::attr("href")').get()
            yield response.follow(pdf_url, self.parse)