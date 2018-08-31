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
        import pdb;
        pdb.set_trace()
        for typecode in ['EAN', 'ISBN']:
            filename = '%s.txt' % typecode
            code = codes[typecode][asin]

            with open(filename, 'a') as f:
                f.write(f"{asin},{code}\n")
            self.log('Saved file %s' % filename)


        # # To get codes from crawler in post_treatment
        # def update_productlookforean(apps, asin_list):
        #
        #     ProductLookForEan = apps.get_model('cia', 'ProductLookForEan')
        #     ProduitEtatMapping = apps.get_model('adminpricing', 'ProduitEtatMapping')
        #     # TODO choose until these soluces
        #     # First soluce
        #     ProductLookForEan.objects.delete(
        #         asin__in=asin_list
        #     )
        #     # Second soluce
        #     ProductLookForEan.objects.filter(
        #         asin__in=asin_list
        #     ).delete()
        #
        #     # Third soluce
        #     products = ProductLookForEan.objects.filter(
        #         asin__in=asin_list
        #     )
        #     for p in products:
        #         with connection.cursor() as cursor:
        #             sql = """
        #             DELETE FROM cia.productlookforean
        #              WHERE asin = %s;
        #             """
        #             try:
        #                 cursor.execute(sql, (p.asin, ))
        #             except Exception as e:
        #                 print(e)
        #     # Fourth soluce
        #     with connection.cursor() as cursor:
        #     sql = """
        #     DELETE FROM cia.productlookforean
        #      WHERE asin in %s;
        #     """
        #     try:
        #         cursor.execute(sql, (p.asin, ))
        #     except Exception as e:
        #         print(e)
        #
        # def update_codeproduit(codes):
        #
        #
        #
        # from cia.models import ProductLookForEan
        # from django.apps import apps
        #
        # def post_treatment():
        #     codes = {'ISBN': {}, 'EAN': {}}
        #     for typecode in ['EAN', 'ISBN']:
        #         filename = '%s.txt' % typecode
        #         with open(filename, 'r') as txt:
        #             for couple in txt.split():
        #                 codes[typecode][couple.split(',')[0]] = couple.split(',')[1]
        #         asin_list = codes[typecode].keys()
        #
        #         # Insert codes found into codeproduit
        #         update_codeproduit(typecode, codes)
        #
        #         # Remove asin from productlookforean
        #         update_productlookforean(apps, asin_list)


