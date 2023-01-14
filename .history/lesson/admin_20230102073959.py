from django.contrib import admin

from .models import Lesson, Instruction, Asset

class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = ({"slug":("title",)})
    
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instruction)
# admin.site.register(Category)
admin.site.register(Asset)
