from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)

    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])


class Wallet(models.Model):
    user_id = models.CharField(max_length=200, db_index=True)
    wallet_adress = models.CharField(max_length=500, db_index=True)

    def __str__(self):
        return self.user_id
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    contract_adress = models.CharField(max_length=200, default="")
    buyer = models.CharField(max_length=200, default="")
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    user_id = models.CharField(max_length=200, default='')
    price = models.DecimalField(max_digits=65, decimal_places=2)
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    product_state = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
