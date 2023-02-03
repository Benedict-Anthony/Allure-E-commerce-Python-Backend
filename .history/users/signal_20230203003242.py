from django.dispatch import receiver
from django.db.models.signals import pre_save
from models import CustomUser


@receiver(pre_save, sender=CustomUser)
def pre_save_user(sender, instance, **kwargs):
    print(instance)
    
    
    

