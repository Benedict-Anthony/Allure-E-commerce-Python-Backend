from django.contrib import admin

from .models import Post

from django.contrib import admin

# from products.models import Category

from .models import Post

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = ({"slug":("title",)})
    
admin.site.register(Post, PostAdmin)

# admin.site.register(Asset)
