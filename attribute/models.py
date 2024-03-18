from django.db import models

# Create your models here.
class Attribute(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices={"color": "color", "normal": "normal"}, default="normal")