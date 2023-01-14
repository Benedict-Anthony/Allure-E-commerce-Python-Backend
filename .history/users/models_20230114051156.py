from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
           raise ValueError(_("email can not be None"))
        if not password:
            raise ValueError(_("password can not be None"))
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
       
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Super user must be set equal to True")) 
        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Staff user must be set equal to True")) 
        if kwargs.get("is_active") is not True:
            raise ValueError(_("Active user must be set equal to True")) 
        
        user = self.create_user(email, password, **kwargs)
        return user



class CustomerUser(AbstractBaseUser, PermissionsMixin):
    gender = [
        ("M","Male"),
        ("F","Female")
        ("O","Other")
    ]
    email = models.EmailField(_("Email Address"), unique=True, max_length=255)
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    gender = models.CharField(_("Gender"), max_length=20, choices=gender)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", last_name]