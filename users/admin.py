from django.contrib import admin

from users.models import CustomUser, Address, UserProfile

admin.site.site_header="Allure Administration"

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Address)
