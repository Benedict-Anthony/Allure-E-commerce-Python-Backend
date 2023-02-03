from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from .models import CustomUser
from .email import confirm_account


@receiver(post_save, sender=CustomUser)
def pre_save_user(sender, instance, created,  **kwargs):
    if created:
        subject = "Allure Account Confirmation"
        email = instance.email
        body = f"Hello {instance.first_name} {instance.last_name}, Thanks for creating an account with allure\n\n"
        
        confirm_account(email, subject, body)
    
    
    
    

