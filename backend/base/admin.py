from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(CustomUser)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_price']