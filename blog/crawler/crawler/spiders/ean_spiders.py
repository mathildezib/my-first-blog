import scrapy


class EanSpider(scrapy.Spider):
    name = "eancrawler"

    # def start_requests(self, urls):
    def start_requests(self):
        urls = [
            'https://mathildezib.pythonanywhere.com/dp/B000E5RKOA',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'ean-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
