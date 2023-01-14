from django.db import models


class AddressDetails(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    description = models.TextField(max_length=100)