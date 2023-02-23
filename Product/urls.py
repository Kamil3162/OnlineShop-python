from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('all/', views.all_products, name='all_products'),
    path('all/product/<int:id>/', views.Product_details.as_view(), name='product_view'),
    path('all/cart/', views.cart_elements, name='cart'),
    path('all/cart/add', views.cart_add, name='add_cart'),
    path('all/cart/<int:id_prod>/del', views.del_from_cart, name='del_cart'),
    path('all/cart/<int:id_prod>/minus', views.cart_count_minus, name='minus_cart'),
    path('all/cart/<int:id_prod>/add', views.cart_count_add, name='adding_cart'),
    path('all/cart/finilize', views.finalize_order, name='order_final'),
    path('all/cart/finilize/validate', views.validate_card, name='order_final_validate'),
    path('all/cart/finilize/success', views.finalize_success, name='order_finish_panel'),
    path('all/category/<str:nazwa>', views.category_products, name='product_category'),
    path('all/complains/', views.ReplyComplains.as_view(), name='product_complain')
    #path('all/listview', views.DisplayProducts.as_view(), name='listview_display'),
    #path('all/<int:id>/detail', views.DetailsProduct.as_view(), name='detail_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)