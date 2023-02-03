from django.db import models

from publik.utils import custom_id

class Post(models.Model):
    id = models.CharField(max_length=30, default=custom_id, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
