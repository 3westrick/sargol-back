from django.db import models
from attribute.models import Attribute

# Create your models here.
class Value(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    color = models.CharField(max_length=9, default=None, null=True, blank=True)