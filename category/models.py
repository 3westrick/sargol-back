from django.db import models

# Create your models here.

def server_product_path(instance, filename):
    print(instance)
    if instance:
        return f"server/{instance.id}/product/{filename}"
    return f"server/desc/product/{filename}"

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    parent = models.ForeignKey('self' ,null=True, on_delete=models.SET_NULL, related_name="children")
    # @property
    # def slug(self):
    #     return "aaa"