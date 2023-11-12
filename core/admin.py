from django.contrib import admin
from .models import *
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Product_in_Order)
admin.site.register(Order)
admin.site.register(Status)