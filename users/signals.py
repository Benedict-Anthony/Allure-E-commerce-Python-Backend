from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from users.token import user_token
from .models import CustomUser
from .email import send_mail


@receiver(post_save, sender=CustomUser)
def pre_save_user(sender, instance, created, **kwargs):
    if created:
        token = user_token({"email": instance.email, "id": instance.id})
        subject = "Allure Account Confirmation"
        email = instance.email
        body = f"""Hello {instance.first_name} {instance.last_name}, 
        Thanks for creating an account with allure\n\n
        To activate your account, please click on the link below:\n\n
        https://allures.vercel.app/comfirm/{token}\n\n
        
        Allure
        
        """

        send_mail(email, subject, body)
