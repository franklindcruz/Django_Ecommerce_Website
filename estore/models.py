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


class Order(models.Model):

    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100, null=False, blank=False)

    email = models.EmailField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    zipcode = models.CharField(max_length=10, null=False, blank=False)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    payment_mode = models.CharField(max_length=100, null=False, blank=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=ORDER_STATUS_CHOICES, default='Pending')
    message = models.TextField(null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} - {} - {}'.format(self.tracking_id, self.user.username, self.status)
       
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} - {} - {}'.format(self.order, self.order.tracking_id, self.quantity)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', null=True, blank=True, default='avatar_pic.jpg')
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username