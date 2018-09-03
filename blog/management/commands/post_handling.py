# -*- coding: utf-8 -*-

import logging
from adminpricing.models import CodeProduit, Produit, TypeCode
from cia.models import ProductLookForEan
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def update_productlookforean(asin_list):
    ProductLookForEan.objects.filter(asin__in=asin_list).delete()


def update_codeproduit(type_code, codes_dict):
    CodeProduit.objects.bulk_create([
        CodeProduit(product=Produit.objects.get(asin=asin),
                    valeur=code,
                    type_code=TypeCode.objects.get(libelle=type_code)
                    )
        for asin, code in codes_dict])


class Command(BaseCommand):
    args = 'loop_forever'
    help = 'Va chercher les infos des produits crawle, puis les insert en bdd'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop_forever', action='store_true', default=False)
        parser.add_argument('--timeout', type=int, default=10)

    def handle(self, *args, **options):
        """
        """

        codes = {'EAN': {}, 'ISBN': {}}
        for typecode in codes.keys():
            logger.info('Get products crawled with an %s code', typecode)
            filename = '%s.txt' % typecode
            with open(filename, 'r') as txt:
                for couple in txt.split():
                    codes[typecode][couple.split(',')[0]] = couple.split(',')[1]

            # Insert codes found into codeproduit
            update_codeproduit(typecode, codes)

            # Remove asin from productlookforean
            asin_list = codes[typecode].keys()
            update_productlookforean(asin_list)
