from django.db import models
from django.utils.translation import gettext_lazy as _
from products.choices import CategoryTypeChoices


class Category(models.Model):
    name = models.IntegerField(primary_key=True,
                               choices=CategoryTypeChoices.choices,
                               default=CategoryTypeChoices.GENERAL,
                               verbose_name=_("Name"))

    def __str__(self):
        return self.get_name_display()

    def __hash__(self):
        return hash(self.name)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    stock = models.IntegerField(verbose_name=_("Stock"))
    category = models.ManyToManyField(Category, related_name="products", verbose_name=_("Category"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
