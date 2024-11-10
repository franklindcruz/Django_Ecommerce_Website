from django.db import models
import datetime
import os
from django.utils.text import slugify
from django.contrib.auth.models import User


def get_file_path(request, filename):
    media_filename = filename
    nowTime = datetime.datetime.now().strftime('%d%m%Y%H:%M:%S')
    filename = "%s%s" % (nowTime, media_filename)
    return os.path.join('categories/', filename)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(
        default=False, help_text="0-inactive, 1-active")
    trending = models.BooleanField(
        default=False, help_text="0-default, 1-trending")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=200, null=False, blank=False)
    meta_description = models.CharField(
        max_length=500, null=False, blank=False)

    slug = models.SlugField(max_length=100, unique=True,
                            null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.name)
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(unique_slug, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    product_image = models.ImageField(
        upload_to='products/', null=True, blank=True)
    product_description = models.CharField(
        max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.CharField(max_length=100, null=False, blank=False)
    available = models.BooleanField(
        default=False, help_text="0-default, 1-available")
    trending = models.BooleanField(
        default=False, help_text="0-default, 1-trending")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=200, null=False, blank=False)
    meta_description = models.CharField(
        max_length=500, null=False, blank=False)

    slug = models.SlugField(max_length=100, unique=True,
                            null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.name)
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(unique_slug, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return self.quantity * (self.product.discount_price if self.product.discount_price else self.product.original_price)

    def __str__(self):
        return self.product.name + ' - ' + self.user.username + ' - ' + str(self.quantity) + ' - ' + str(self.get_total())
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name + ' - ' + self.user.username