from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from .models import CustomUser
from .email import confirm_account


@receiver(pre_save, sender=CustomUser)
def pre_save_user(instance, **kwargs):
    print(kwargs)
    
    
    

