from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save

from users.token import user_token
from .models import CustomUser
from .email import confirm_account


@receiver(post_save, sender=CustomUser)
def pre_save_user(sender, instance, created,  **kwargs):
    if created:
        token = user_token({"email":instance.email, "id":instance.id})
        subject = "Allure Account Confirmation"
        email = instance.email
        body = f"""Hello {instance.first_name} {instance.last_name}, Thanks for creating an account with allure\n\n
        
        To confirm your account, please click on the link below:\n\n
        
        http://127.0.0.1:3000/api/user/confirm/{token}\n\n
        
        """
        
        confirm_account(email, subject, body)
    
    
    
    

