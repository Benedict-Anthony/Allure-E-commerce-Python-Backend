from django.contrib import admin

from users.models import CustomUser, Address

admin.site.site_header="Allure Administration"

admin.site.register(CustomUser)
admin.site.register(Address)
