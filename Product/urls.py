from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_products, name='all_products'),
    path('all/product/<int:id>/', views.Product_details.as_view(), name='product_view'),
    path('all/cart/', views.cart_elements, name='cart'),
    path('all/cart/add', views.cart_add, name='add_cart'),
    path('all/cart/<int:id_prod>/del', views.del_from_cart, name='del_cart'),
    path('all/cart/<int:id_prod>/minus', views.cart_count_minus, name='minus_cart')

]