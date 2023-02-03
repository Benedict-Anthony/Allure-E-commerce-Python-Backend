from  django.despatch  import  receiver
from django.signal import post_save, pre_save
from user.models import CustomUser


@receiver(pre_save, sender=CustomUser)
def pre_save_user(sender, instance, **kwargs):
    print(instance)
    
    
    

