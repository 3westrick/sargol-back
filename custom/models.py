from django.db import models

# Create your models here.
class Custom(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)