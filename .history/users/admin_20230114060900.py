from django.contrib import admin

from users.models import CustomUser

admin.site.site_header("Allure Administration")

admin.site.register(CustomUser)
