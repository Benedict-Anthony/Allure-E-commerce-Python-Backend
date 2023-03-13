from django.db import models

from publik.utils import custom_id
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from products.models import Products
from publik.utils import custom_id

    

class Post(models.Model):
    id = models.CharField(max_length=30, default=custom_id, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=100, blank=True, null=True )
    description = models.TextField(max_length=400)
    assets = models.ManyToManyField(Products, blank=True)
    image = models.ImageField(upload_to="images", default="", blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True, null=True, default="")
    slug = models.SlugField(blank=True, null=True, default="", unique=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title
    
    
    def topics(self):
        return self.category
    
    
    @property
    def image_url(self):
        try:
            image = self.image.url
        except :
            image = ""
            
        return image
    
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(image=self.image)
                self.save()
                return self.thumbnail.url
        
        return ""

        
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io,"PNG", quality=85)
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail
        
        
 
    
