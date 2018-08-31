from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class ProductLookForEan(models.Model):
    productlookforean_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Produit', db_column='product_id_fk')
    marketplace = models.ForeignKey('Plateforme', blank=False, null=False, db_column='marketplace_id_fk')

    class Meta:
        app_label = 'cia'
        db_table = 'productlookforean'

    def __str__(self):
        return str(self.product) + ' - ' + str(self.marketplace)