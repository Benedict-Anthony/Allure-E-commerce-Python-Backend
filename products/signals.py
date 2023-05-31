from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Products
from users.email import send_mail
from users.models import CustomUser
from blog.models import Post


@receiver(post_save, sender=Products)
def nofity_users(sender, instance, created, **kwargs):
    if instance.notify:
        subject = f"New Product Added - {instance.name}"
        body = f"""
        Hi there,
        
        Check out our new product {instance.name} at {instance.price} 
        
        https://allures.vercel.app/products/{instance.slug}/
        
        Trust Allure, it's amazing and you will love it.
        
        Thank you for choosing us
        
        """
        instance.notify = False
        instance.notified = True
        instance.save()
        for users in CustomUser.objects.all():
            send_mail(email=users.email, subject=subject, body=body)


@receiver(pre_save, sender=Products)
def make_thumbnail(sender, instance, **kwargs):
    instance.thumbnail = instance.image
    return instance


@receiver(pre_save, sender=Post)
def make_thumbnail(sender, instance, **kwargs):
    instance.thumbnail = instance.image
    return instance
