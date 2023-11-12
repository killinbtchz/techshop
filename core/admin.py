from django.contrib import admin
from .models import *

class ProductInOrderAdmin(admin.ModelAdmin):
    #search_fields = ('kind',)
    list_filter = ('order',)
    list_display = ('id', 'order', 'product', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    #search_fields = ('kind',)
    list_filter = ('user', 'status', 'date')
    list_display = ('id', 'user', 'adress', 'status', 'date', 'price', 'quantity')


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Product_in_Order, ProductInOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Status)
