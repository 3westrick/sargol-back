from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=50, blank=True)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Region(models.Model):
    label = models.CharField(max_length=80, blank=True)
    code = models.CharField(max_length=4, blank=True, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    suggested = models.BooleanField(default=False)