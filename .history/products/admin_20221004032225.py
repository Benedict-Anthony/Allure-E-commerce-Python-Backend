from django.contrib import admin

from .models import Products, OrderDetails, AddressDetails, Customer

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = ({"slug":("name",)})
    
admin.site.register(Products, ProductAdmin)
admin.site.register(OrderDetails)
admin.site.register(AddressDetails)
admin.site.register(Customer)