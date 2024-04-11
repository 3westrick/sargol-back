from django.db import models
from attribute.models import Attribute
from category.models import Category

# Create your models here.
WIDGET_TYPES = [
    ('attribute', 'attribute'),
    ('category', 'category'),
    ('price', 'price'),
    ('rating', 'rating'),
]

DISPLAY = [
    ('list', 'list'),
    ('dropdown', 'dropdown'),
]

class WidgetGroup(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=200)

class Widget(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey(WidgetGroup, on_delete=models.CASCADE, related_name="widgets")
    type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="widgets", null=True, blank=True)
    display = models.CharField(max_length=50, choices=DISPLAY, default='list')


# class WidgetGroup(models.Model):
#     type = models.CharField(max_length=200)

# class Widget(models.Model):
#     group = models.ForeignKey(WidgetGroup, on_delete=models.CASCADE, related_name="widgets")
#     key = models.CharField(max_length=200, null=True, blank=True)
#     value = models.CharField(max_length=200, null=True, blank=True)
