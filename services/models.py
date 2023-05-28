from django.db import models
from publik.utils import custom_id
from users.models import CustomUser
from django.utils.text import slugify

class Category(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=custom_id, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="services")
    slug = models.SlugField(unique=True, max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    
class Service(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=custom_id, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    image = models.ImageField(upload_to="services")
    slug = models.SlugField(unique=True, max_length=100)
    
    def __str__(self):
        return self.name

class Bookings(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=custom_id, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_bookings")
    date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=[("pending", "pending"), ("completed", "completed"), ("cancelled", "cancelled")], default="pending")
    description = models.TextField()
    slug = models.SlugField(max_length=100)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.service.name}-{self.id}")
        return super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name_plural = "Bookings"
        ordering = ["-date"]
        
    def __str__(self):
        return self.service.name