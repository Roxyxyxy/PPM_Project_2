from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Customer

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)