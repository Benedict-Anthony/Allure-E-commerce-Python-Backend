from django.contrib import admin
from .models import Category, Service, Bookings

class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Service, ServiceAdmin)


class BookingsAdmin(admin.ModelAdmin):
    list_display = ["user", "service", "date", "location", "status"]
    list_filter = ["status", "date"]

admin.site.register(Bookings, BookingsAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
     
admin.site.register(Category, CategoryAdmin)  