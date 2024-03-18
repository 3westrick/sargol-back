from typing import Any, Optional
from django.core.management.base import BaseCommand
from base.models import User
# from django.contrib.auth.models import User
import os, glob
from pathlib import Path
import random

# from product.models import Product
from category.models import Category
from attribute.models import Attribute
from value.models import Value

import subprocess

def create_attributes_value():
    attributes = {
            'Color': ['Red', 'Blue', 'Green'],
            'Size' : ['Sm', 'Ms', 'Lg', 'Xl'],
            'Hard' : ['1tb', '2tb', '3tb'],
        }
    for key in attributes.keys():
        att = Attribute.objects.create(title=key, is_active=True, slug=key.lower())
        for value in attributes[key]:
            att.values.create(title=value, is_active=True, slug=value.lower())


def create_products():
    titles = ['product 1', 'product 2', 'product 3']
    for title in titles:
        pro = Product.objects.create(title=title,price=10000 ,slug=title.replace(' ', '-'), is_active=True, category=Category.objects.get(pk=random.randint(1, 3)))
        # pro.gallery.create(image="server/None/product/aa.jpeg.webp")

def create_categories():
    categories = ['cat 1', 'cat 2', 'cat 3']
    for category in categories:
        Category.objects.create(title=category, slug=category.replace(' ', '-'))

class Command(BaseCommand):
    help = "Display hello"

    def handle(self, *args: Any, **options: Any) -> str | None:

        for i in Path('.').glob('*/migrations/*_initial.py'):
            os.remove(i)
        if os.path.exists("db.sqlite3"): os.remove("db.sqlite3")

        result = subprocess.run(["python", "manage.py", "makemigrations"], capture_output=True, text=True)
        output = result.stdout
        print(output)

        result = subprocess.run(["python", "manage.py", "migrate"], capture_output=True, text=True)
        output = result.stdout
        print(output)


        create_attributes_value()

        create_categories()
        
        # create_products()

        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        # user.set_password("admin")
        # user.phone = "09117607570"
        user.save()
 

