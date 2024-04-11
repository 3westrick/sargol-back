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
from product.models import Product
from widget.models import WidgetGroup, Widget

import subprocess

alpha = 'abcdefghijklmnopqrstuvwxyz'
categories_id = [1,2,3,4,5,6,7,8,10,11]
atts = [1,2,3]
vals = [1,2,3,4,5,6,7,8,9,10]

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
    variant_names = [
        'Rustic Concrete Cheese','Refined Frozen Mouse',

        'Practical Wooden Fish','Practical Concrete Sausages',

        'Unbranded Soft Hat','Refined Cotton Gloves',

        'Incredible Granite Fish','Licensed Plastic Table',

        'Refined Cotton Table','Incredible Plastic Table',

        'Generic Granite Soap','Tasty Concrete Soap',
    ]
    simple_product = ['Refined Cotton Ball', 'Unbranded Granite Towels', 'Refined Soft Ball',
                       'Unbranded Metal Salad', 'Sleek Cotton Pants', 'Incredible Wooden Towels',
                         'Licensed Cotton Car', 'Generic Metal Salad', 'Ergonomic Wooden Ball',
                         'Intelligent Frozen Towels', 'Handmade Cotton Tuna', 'Tasty Soft Computer',
                         ]
    variant_product = ['Small Wooden Chicken', 'Gorgeous Fresh Chips', 'Refined Granite Pants', 'Fantastic Metal Hat', 'Table', 'Soap']
    random.choices
    for i, product in enumerate(simple_product):
        p = Product.objects.create(
            title=product,
            slug=product.replace(' ', '-').lower(),
            type='simple',
            short_description='Ergonomic executive chair upholstered in bonded black leather and PVC padded seat and back for all-day comfort and support',
            description='<p>The slim & simple Maple Gaming Keyboard from Dev Byte comes with a sleek body and 7- Color RGB LED Back-lighting for smart functionality</p>',
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class="standard",
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            stock=10,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class='no_shipping_class',
            image='/camera.png'
            )
        p.categories.add(*random.choices(population=categories_id, k=random.randint(2,4)))
        if i % 3 == 0:
            p.attributes.create(attribute_id=1, variant=False, visible=True)
            p.values.add(*random.choices(population=[1,2,3], k=2))
        if i % 3 == 1:
            p.attributes.create(attribute_id=2, variant=False, visible=True)
            p.values.add(*random.choices(population=[4,5,6,7], k=2))
        if i % 3 == 2:
            p.attributes.create(attribute_id=1, variant=False, visible=True)
            p.values.add(*random.choices(population=[1,2,3], k=2))

            p.attributes.create(attribute_id=2, variant=False, visible=True)
            p.values.add(*random.choices(population=[4,5,6,7], k=2))

    i = 0
    for j, parent_product in enumerate(variant_product):
        c = random.choices(population=categories_id, k=random.randint(2,4))

        product = Product.objects.create(
            title=parent_product,
            slug=parent_product.replace(' ', '-').lower(),
            type='variation',
            short_description='Ergonomic executive chair upholstered in bonded black leather and PVC padded seat and back for all-day comfort and support',
            description='<p>The slim & simple Maple Gaming Keyboard from Dev Byte comes with a sleek body and 7- Color RGB LED Back-lighting for smart functionality</p>',
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class="standard",
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            stock=10,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class='no_shipping_class',
            image='/camera.png'
            )
        
        product.categories.add(*c)
        if j % 3 == 0:
            product.attributes.create(attribute_id=1, variant=True, visible=True)
            product.values.add(1,2)
        if j % 3 == 1:
            product.attributes.create(attribute_id=2, variant=True, visible=True)
            product.values.add(4,5)
        if j % 3 == 2:
            product.attributes.create(attribute_id=1, variant=True, visible=True)
            product.values.add(2,3)

        # print(product.values.all())
        variant = product.variants.create(
            title=variant_names[i],
            slug=variant_names[i].replace(' ', '-').lower(),
            type='vartiant',
            short_description=product.short_description,
            description=product.description,
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class="standard",
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            quantity=10,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class='no_shipping_class',
            image='/camera.png'
        )

        variant.categories.add(*c)
        for p_a in product.attributes.all():
            variant.attributes.create(attribute=p_a.attribute, visible=True, variant=True)
        variant.values.add(product.values.all()[0])
        i+=1

        variant = product.variants.create(
            title=variant_names[i],
            slug=variant_names[i].replace(' ', '-').lower(),
            type='vartiant',
            short_description=product.short_description,
            description=product.description,
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class="standard",
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            stock=10,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class='no_shipping_class',
            image='/camera.png'
        )

        variant.categories.add(*c)
        for p_a in product.attributes.all():
            variant.attributes.create(attribute=p_a.attribute, visible=True, variant=True)
        variant.values.add(product.values.all()[1])
        i+=1


def create_categories():
    categories =['Grocery',
    'Games',
    'Garden',
    'Industrial',
    'Computers',
    'Kids',
    'Music',
    'Jewelery',
    'Baby',
    'Beauty',
    'Movies',
    'Outdoors',]
    
    for category in categories:
        Category.objects.create(title=category, slug=category.replace(' ', '-').lower())


def create_widget():
    wg = WidgetGroup.objects.create(type='shop_page_widget_area', title='Shop page widget area')
    wg.widgets.create(
        type="category",
        title='Category',
        # display='list',
    )

    wg.widgets.create(
        type="attribute",
        title='Color',
        attribute=Attribute.objects.get(pk=1),
        # display='list',
    )

    wg.widgets.create(
        type="attribute",
        title='Size',
        attribute=Attribute.objects.get(pk=2),
        # display='list',
    )
    wg.widgets.create(
        type="price",
        title='Price',
        # display='list',
    )
    wg.widgets.create(
        type="rating",
        title='Rating',
        # display='list',
    )


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
        
        create_products()

        create_widget()

        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        user.set_password("admin")
        # user.phone = "09117607570"
        user.save()
 

