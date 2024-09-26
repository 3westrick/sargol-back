from django.db import models

# Create your models here.
class Option(models.Model):
    title = models.TextField(max_length=50)
    value = models.TextField(max_length=50)