from django.urls import path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('admin/', admin.site.urls),
    path('products/', views.products, name='products'),
    path('products/product<int:id>/', views.product, name='product'),
    path('categories/', views.categories, name='categories'),
    path('categories/category<int:id>/', views.products, name='products_by_category'),
    path('brands/', views.brands, name='brands'),
    path('brands/brand<int:id>/', views.brands, name='products_by_brand'),
    path('import_data/', views.import_data, name='import_data'),
    path('del_all/', views.del_all, name='del_all'),
    path('dellme/', views.dellme, name='dellme'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart/', views.cart, name='cart_detail'),
    path('clear/', views.clear),
    path('checkout', views.checkout, name='checkout'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),
    path('get_resized_cart_icon/', views.get_resized_cart_icon, name='get_resized_cart_icon'),
    path('orders/', views.orders, name='orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('arm_op/', views.arm_op, name='arm_op'),
    path('get_resized_cart_icon1/', views.get_resized_cart_icon1, name='get_resized_cart_icon1'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('delme', views.delme),
    path('test', views.test),
    path('api/product/', views.ProductListCreate.as_view() ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
