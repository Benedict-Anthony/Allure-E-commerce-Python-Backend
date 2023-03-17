from django.db.models.signals import post_save
from .models import Bookings
from django.dispatch import receiver
from users.email import send_mail


@receiver(post_save, sender=Bookings)
def send_booking_email(sender, instance, created, **kwargs):
    if created:
        email = instance.user.email
        subject = f"Booking For {instance.service.name} Confirmed"
        body = f"""
        Hi {instance.user.first_name} {instance.user.last_name},
        
        Your booking has been confirmed. We will get back to you shortly for negotiations and other details.
        
        
        Thank you for choosing us
        
        Allure
        """
        send_mail(email=email, subject=subject, body=body)
        

