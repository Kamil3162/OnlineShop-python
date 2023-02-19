from django.contrib import admin
from .models import (Product,
                     Producer,
                     Rate,
                     Category,
                     Order,
                     OrderItem,
                     ShipAddress)

admin.site.register(Producer)

admin.site.register(Product)


admin.site.register(Category)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']
    search_fields = ['customer']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order']

@admin.register(ShipAddress)
class ShipAddressAdmin(admin.ModelAdmin):
    list_display = ['order', 'user']
    search_fields = ['user']

@admin.register(Rate)
class ShipAddressAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rate']
    search_fields = ['product']

'''
@admin.register(Complain)
class ComplainApplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'subject']
    search_fields = ['user']
'''
