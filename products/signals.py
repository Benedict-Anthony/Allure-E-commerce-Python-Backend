from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Products
from users.email import send_mail
from users.models import CustomUser


@receiver(post_save, sender=Products)
def nofity_users(sender, instance, created, **kwargs):
    if instance.notify:
        subject = f"New Product Added- {instance.name}"
        body = f"""
        Hi there,
        
        Check out our new product {instance.name} at {instance.price} 
        
        https://localhost:3000/products/{instance.slug}/
        
        Trust Allure, it's amazing and you will love it.
        
        Thank you for choosing us
        
        """
        instance.notify = False
        instance.notified = True
        instance.save()
        for users in CustomUser.objects.all():
            send_mail(email=users.email, subject=subject, body=body)
            
   