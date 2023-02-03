from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from products.models import Products
from publik.utils import custom_id


class Asset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    uses = models.TextField(max_length=50)
 
    
    def __str__(self):
        return self.name
    
    
class Instruction(models.Model):
    step = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images")
    content = models.TextField(max_length=200, default="")

    def __str__(self):
        return self.step

class Lesson(models.Model):
    type = [
        ("Free", "Free"),
        ("Premium", "Premium"),
    ]
    level = [
        ("Begginner", "Begginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]
    id = models.CharField(max_length=100, default=custom_id, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    assets = models.ManyToManyField(Products, blank=True)
    instructions = models.ManyToManyField(Instruction)
    image = models.ImageField(upload_to="images", default="", blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True, null=True, default="")
    level = models.CharField(max_length=20, choices=level, default="Begginner")
    type = models.CharField(max_length=20, choices=type, default="Free")
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
        
        
        
        
        
            
# class Package(models.Model):
#     title = models.CharField(max_length=255)
#     price = models.FloatField()
              


# class Services(models.Model):
#     name = models.CharField(max_length=70)
#     excerpt = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to="services")
#     thumbnail = models.ImageField(upload_to="services")
#     price_1 = models.FloatField()
#     price_2 = models.FloatField()
#     slug = models.SlugField(max_lenth=255, unique=True)
    # serviceDetails = models.ForeignKey(ServicesDetails, on_delete=models.CASCADE, related_name="services_details")
    
    
