from django.shortcuts import render, HttpResponse
from django.db.models import Q
from .models import *
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from django.http import JsonResponse
from PIL import Image
from .serializers import ProductSerializer
from rest_framework import generics




def index(request):
    context = {}
    context['discount_products'] = Product.objects.all()[:4]
    context['categories'] = Category.objects.all()
    return render(request, 'core/index.html')

def del_all(request):
    for product in Product.objects.all():
        product.delete()
    return HttpResponse('OK')


def import_data(request):
    if request.method == 'POST':
        data = request.POST['data']
        data = data.split('\r\n')
        i = 0
        while i < len(data)-3:
            cur = data[i].split(';')
            next2 = data[i+2].split(';')
            if next2[0] == 'Наименование':
                category_name = cur[0]
                i += 3
            else:
                text, price, trash = cur
                a = text.split()
                name = ' '.join(a[1:])
                brand_name = a[1]
                try:
                    price = int(price.replace('p.',''))
                except:
                    price = None
                if price:
                    category, exists = Category.objects.get_or_create(name=category_name)
                    product = Product(name=name, price=price, category=category, availability=True)
                    product.save()
                    brand, exists = Brand.objects.get_or_create(name=brand_name)
                    tag, exists = Tag.objects.get_or_create(name=brand_name)
                    product.tag.add(tag)
                    product.save()
                i += 1

    return render(request, 'core/import_data.html')


def products(request):
    context = {}
    context['products'] = Product.objects.all() [:200]
    context['categories'] = Category.objects.all()
    context['brands'] = Brand.objects.all()
    print(request.POST, request.GET, request.method)
    if request.method == 'GET':
        filter_data = request.GET
    else:
        filter_data = request.POST

    products = Product.objects.all()
    if filter_data:
        if 'brands' in filter_data:
            brands = filter_data['brands'].split(',')
            if brands:
                tag = Tag.objects.get(name=brands[0])
                products = tag.products.all()
                for tag_id in brands[1:]:
                    tag = Tag.objects.get(name=tag_id)
                    products = products | tag.products.all()

        if 'categories' in filter_data:
            cats = filter_data['categories'].split(',')
            if cats:
                products = products.filter(category__in=cats)

    context['products'] = products

    if request.method == 'POST':
        return render(request, 'core/products_list.html', context)
    else:
        return render(request, 'core/products.html', context)




def categories(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'core/categories.html', context)


def product(request, id):
    context = {}
    context['product'] = Product.objects.get(id=id)
    return render(request, 'core/product.html', context)


def brands(request):
    context = {}
    context['brands'] = Brand.objects.all()
    return render(request, 'core/brands.html', context)


def dellme(request):
    context = {}
    return render(request, 'core/dellme.html')


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        print('add')
        product_id = str(product.id)
        if product_id not in self.cart:
            print('new_product')
            self.cart[product_id] = {'quantity': 0, 'price': int(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.cart[product_id]['totalprice'] = self.cart[product_id]['price'] * self.cart[product_id]['quantity']
        print(self.cart)
        print('end add')
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(item['totalprice'] for item in self.cart.values())

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def remove_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_quantity_product_in_cart(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        else:
            return 0

    def test(self):
        return 'Hello!'



@require_POST
def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST['product_id'])
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=False)
    return HttpResponse('OK')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'message': 'Cart cleared successfully'})


def cart_remove(request):
    product_id = request.POST.get('product_id')
    cart = Cart(request)
    cart.remove_product(product_id)
    return JsonResponse({'success': True})


def cart(request):
    cart = Cart(request)
    for item in cart:
        print(item)
    return render(request, 'core/cart.html', {'cart': cart})

def clear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse('Ok')


def checkout(request):
    cart = Cart(request)
    return render(request, 'core/checkout.html', {'cart': cart})


@require_POST
def cart_update(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST['product_id'])
    quantity_change = int(request.POST['quantity_change'])
    current_quantity = cart.cart[str(product.id)]['quantity']
    new_quantity = max(current_quantity + quantity_change, 0)
    cart.add(product=product, quantity=new_quantity, update_quantity=True)

    context = {
        'product_quantity': new_quantity,
        'product_total_price': cart.cart[str(product.id)]['totalprice'],
        'total_price': cart.get_total_price(),
        'total_quantity': len(cart),
    }

    return JsonResponse(context)


def get_resized_cart_icon(request):
    image_path = 'static/pngwing.com (50).png'
    img = Image.open(image_path)
    img = img.resize((30, 30), Image.Resampling.LANCZOS)

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def get_resized_cart_icon1(request):
    image_path = 'static/pngwing.com (54).png'
    img = Image.open(image_path)
    img = img.resize((20, 20), Image.Resampling.LANCZOS)

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def orders(request):
    print('orders')
    context = {}
    context['orders'] = Order.objects.all()
    cart = Cart(request)
    context['cart'] = cart
    print(context)
    return render(request, 'core/orders.html', context)


def create_order(request):
    status = Status.objects.get(status='Новый')
    cart = Cart(request)
    order = Order.objects.create(status=status, user=request.user, adress='asdfasdf Адрес ', price=cart.get_total_price(), quantity=len(cart))
    for item in cart:
        Product_in_Order.objects.create (order=order,product=item['product'],quantity=item['quantity'], price=item['price']).save()
    cart.clear()
    return HttpResponse('ok')


def arm_op(request):
    context = {}
    context['orders'] = Order.objects.all()
    context['statuses'] = Status.objects.all()
    cart = Cart(request)
    context['cart'] = cart
    print(context)
    return render(request, 'core/arm_op.html', context)


def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        order = Order.objects.get(id=order_id)
        status = Status.objects.get(id=new_status)
        order.status = status
        order.save()

        return HttpResponse(status.status)


def delme(request):
    return render(request, 'core/delme.html')


def test(request):
    return render(request, 'core/test.html')




class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



