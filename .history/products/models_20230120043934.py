from django.db import models
from django.db.models import Q
from users.models import Address
from PIL import Image
from io import BytesIO
from django.core.files import File

from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class ProductQueryset(models.QuerySet):
    def is_available(self):
        return self.filter(available=True)
class ProductManager(models.Manager):
    def search(self, query):
        if query:
            return self.filter(Q(name__icontains=query) | Q(slug__icontains=query))
        return []
    
    
    def get_queryset(self, args, kwargs):
        return ProductQueryset(self.model, using=self._db)
    
class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to="images", default="")
    thumbnail = models.ImageField(upload_to="thumbnails", default="", blank=True, null=True)
    percent = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=400)
    rating =models.IntegerField(default=1, blank=True, null=True)
    category =  models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL,null=True )
    slug = models.SlugField(blank=True, null=True, default="", unique=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    objects = models.Manager()
    available_products = ProductManager()
    
    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return ""
    
    @property
    def product_discount(self):
        if self.discount:
            return self.discount
        else:
            return 0.0
        
    @property
    def product_price(self):
        if self.discount:
            return self.price - self.discount
        
        return self.price
    
    @property
    def disc_perc(self):
        if self.discount:
            self.percent = round((float(self.discount) / float(self.price)) * 100, 1)
            self.save()
            return self.percent
        return 0
    

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
        img.save(thumb_io, "PNG", quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
      
    class Meta:
        verbose_name_plural = "Products"
        ordering =("-created",)
   
    
    def __str__(self):
        return self.name

class OrderDetails(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    address_details = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=4, decimal_places=2)
    
    
    class Meta:
        verbose_name_plural = "Order Items Details"