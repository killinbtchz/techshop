from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/category/' + self.slug


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    availability = models.CharField(max_length=255, blank=True, null=True)
    tag = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/products/product' + str(self.id)


class Brand(models.Model):
    name = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/brands/brand' + str(self.id)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
    main = models.BooleanField(default=False)


class Status(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class Product_in_Order(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adress = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=Product_in_Order)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)




