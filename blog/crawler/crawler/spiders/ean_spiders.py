# -*- coding: utf-8 -*-


import scrapy
from bs4 import BeautifulSoup


class EanSpider(scrapy.Spider):
    name = "eancrawler"

    # def start_requests(self, urls):
    def start_requests(self):
        urls = [
            'https://mathildezib.pythonanywhere.com/dp/B000E5RKOA',
            'http://mathildezib.pythonanywhere.com/dp/B00SU78O6W',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        asin = response.url.split("/")[-1]
        filename = 'ean-%s.html' % asin
        html = BeautifulSoup(response.body, "lxml")
        details = html.find("div", {"id": "detail_bullets_id"})
        params = details.find_all('li')
        codes = {'ISBN': {}, 'EAN': {}}
        codes['ISBN'][asin] = None
        codes['EAN'][asin] = None
        for param in params:
            if 'ISBN' in str(param) or 'EAN' in str(param):
                code = str(param).split()[1].strip('</li>')
                if len(code) == 13:
                    codes['EAN'][asin] = code
                    codes['ISBN'][asin] = code
                elif len(code) == 9:
                    codes['ISBN'][asin] = code
        for typecode in ['EAN', 'ISBN']:
            filename = '%s.txt' % typecode
            code = codes[typecode][asin]

            with open(filename, 'a') as f:
                f.write(f"{asin},{code}\n")
            self.log('Saved file %s' % filename)




