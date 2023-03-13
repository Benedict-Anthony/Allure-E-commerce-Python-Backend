from django.contrib import admin

from .models import Products, Order, Category, OrderedItems

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = ({"slug":("name",)})
    
admin.site.register(Products, ProductAdmin)

class OrderedItemsAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "quantity", "price", "transaction_id","date",)
admin.site.register(OrderedItems,OrderedItemsAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "order", "address", "total_price", "status", "complete", "date",)
    list_filter = ( "order", "address", "status", "complete", "date",)
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)