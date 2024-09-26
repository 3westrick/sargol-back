from typing import Any, Optional
from django.core.management.base import BaseCommand
from base.models import User
# from django.contrib.auth.models import User
import os, glob
from pathlib import Path
import random
from utils import countries
from option.models import Option

# from product.models import Product
from category.models import Category
from attribute.models import Attribute
from value.models import Value
from shipping.models import Shipping, Zone
from tax.models import Tax, Rate
from product.models import Product
from coupon.models import Coupon
from datetime import date, timedelta
from base.models import Region

from widget.models import Widgetgroup as wg, Widget as w

import subprocess

alpha = 'abcdefghijklmnopqrstuvwxyz'
categories_id = [1,2,3,4,5,6,7,8,10,11]
atts = [1,2,3]
vals = [1,2,3,4,5,6,7,8,9,10]

def create_regions():
    for country in countries:
        Region.objects.create(label=country.get('label'), code=country.get('code'), phone=country.get('phone'), suggested=country.get('suggested', False))

def create_widgettest():
    group = wg.objects.create(title='shop page widget area', slug='shop_page_widget_area')

    group.create_attribute(1, title='Color', display='list')
    group.create_attribute(2, title='Size', display='list')
    
    group.create_category(title='Product category', display='list')

    group.create_price(title='Product price', apply_filter=None, type='text')

    group.create_rating(title='Product Rating')

    widgets = group.get_widgets()
    # print(widgets)


def create_shipping():
    Shipping.objects.create(
        title='No shipping class',
        slug='no-shipping-class',
        description='no ship',
        # price=0
    )

    Shipping.objects.create(
        title='big',
        slug='big',
        description='big ship',
        # price=20
    )
    Shipping.objects.create(
        title='tall',
        slug='tall',
        description='tall ship',
        # price=20
    )
    Shipping.objects.create(
        title='short',
        slug='short',
        description='short ship',
        # price=10
    )

    Zone.objects.create(
        name='rest of the word'
    )

def create_tax():
    Tax.objects.create(
        title='standard',
    )
    Tax.objects.create(
        title='shoes',
    )
    Tax.objects.create(
        title='jackets',
    )

def create_rates():
    pass
    # Rate.objects.create(
    #     tax=Tax.objects.get(pk=1),
    #     country='AF',
    #     states='aaa',
    #     zip_code='bbb',
    #     # cities='ccc',
    #     name='ddd',
    #     rate=20,
    #     on_shipping=True,
    # )
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
            tax_class=Tax.objects.get(pk=1),
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            quantity=10,
            stock=0,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class=Shipping.objects.get(pk=1),
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
            tax_class=Tax.objects.get(pk=1),
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=True,
            stock_status='in_stock',
            sold_individually=False,
            quantity=10,
            stock=0,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class=Shipping.objects.get(pk=1),
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
            type='variant',
            short_description=product.short_description,
            description=product.description,
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class=Tax.objects.get(pk=1),
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=product.stock_management,
            stock_status='in_stock',
            sold_individually=False,
            quantity=10,
            stock=0,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class=Shipping.objects.get(pk=1),
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
            type='variant',
            short_description=product.short_description,
            description=product.description,
            regular_price=random.randint(25, 150),
            sale_price=0,
            tax_status="taxable",
            tax_class=Tax.objects.get(pk=1),
            sku=''.join(random.choices(population=alpha, k=8)),
            mpn=''.join(random.choices(population=alpha, k=6)),
            stock_management=product.stock_management,
            stock_status='in_stock',
            sold_individually=False,
            quantity=10,
            stock=0,
            unit='pair',
            weight=10,
            length=10,
            width=10,
            height=10,
            shipping_class=Shipping.objects.get(pk=1),
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


def create_coupons():

    Coupon.objects.create(
        title='xyz',
        description='xyz',
        type=Coupon.CouponTypes.PERCENTAGE,
        amount=20,
        expired_at=date.today() + timedelta(days=4),
        minimum = -1,
        maximum = -1,
        individual_use = False,
        exclude_sale_items = False,
        usage_limit= -1,
        item_limit= -1,
        user_limit= -1,
    )

    Coupon.objects.create(
        title='aa',
        description='aa',
        type=Coupon.CouponTypes.FIXED_PRODUCT,
        amount=10,
        expired_at=date.today() + timedelta(days=4),
        minimum = -1,
        maximum = -1,
        individual_use = False,
        exclude_sale_items = False,
        usage_limit= -1,
        item_limit= -1,
        user_limit= -1,
    )


def create_options():
    # Option.objects.create(title = 'shipping_calculations', value = 'enable_on_basket_page')
    Option.objects.create(title = 'shipping_destination', value = 'default_shipping_address')
    Option.objects.create(title = 'price_entered_with_tax', value = 'yes')
    Option.objects.create(title = 'display_prices_in_the_shop', value = 'include')
    Option.objects.create(title = 'display_prices_during_basket_and_checkout', value = 'include')

    Option.objects.create(title = 'selling_locations', value = 'all_countries')
    Option.objects.create(title = 'specific_countries', value = '')
    Option.objects.create(title = 'exception_countries', value = '')
    Option.objects.create(title = 'shipping_locations', value = 'ship_to_all_countries_you_sell_to')
    Option.objects.create(title = 'shipping_countries', value = '')


def div():
    print('---------'*3)

class Command(BaseCommand):
    help = "Display hello"

    def handle(self, *args: Any, **options: Any) -> str | None:

        for i in Path('.').glob('*/migrations/*_initial.py'):
            os.remove(i)
        if os.path.exists("db.sqlite3"): os.remove("db.sqlite3")

        result = subprocess.run(["python", "manage.py", "makemigrations"], capture_output=True, text=True)
        output = result.stdout
        # print(output)

        result = subprocess.run(["python", "manage.py", "migrate"], capture_output=True, text=True)
        output = result.stdout
        div()
        print("Tables Created")
        div()

        create_regions()
        print("Regions Created")
        div()
        # print(output)


        create_attributes_value()
        print("Attribute / Values Created")
        div()

        create_categories()
        print("Categories Created")
        div()

        create_shipping()
        print("Shipping Classes Created")
        div()

        create_tax()
        create_rates()
        print("Tax Classes Created")
        div()
        
        create_products()
        print("Products Created")
        div()


        create_coupons()
        print("Coupons Created")
        div()

        create_widgettest()
        print("Widgets Created")
        div()


        create_options()
        print("Options Created")
        div()


        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        user.set_password("admin")
        # user.phone = "09117607570"
        user.save()
        print("Admin USer Created")
        div()
 

