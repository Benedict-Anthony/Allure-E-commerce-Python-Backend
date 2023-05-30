import secrets
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext as _

from publik.utils import custom_id

# from publik.utils import custom_id


class Address(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.state} - {self.city}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("email can not be None"))
        # if not password:
        #     raise ValueError(_("password can not be None"))
        # kwargs.setdefault("is_active", True)

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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    gender = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    id = models.CharField(
        primary_key=True, default=custom_id, editable=False, max_length=32, unique=True
    )
    email = models.EmailField(_("Email Address"), unique=True, max_length=255)
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    gender = models.CharField(_("Gender"), max_length=20, choices=gender)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name_plural = "Users"

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_profile"
    )
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    avatar = models.ImageField(null=True, blank=True, upload_to="profile")
