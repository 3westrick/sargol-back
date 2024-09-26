from rest_framework import generics
from base.mixins import CheckAuth
from coupon.models import Coupon
from coupon.serial import CouponSerial
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, ValidationError
from datetime import date
from order.models import Item
from time import process_time
from product.models import Product

class CouponRetrieveView(CheckAuth ,generics.RetrieveAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerial
    lookup_field = 'title'
    



def product_discount_price(item, coupon, product_price):
    if coupon.type == 'fixed_product':
        if item.product.sale_price != 0:
            if coupon.exclude_sale_items:
                pass
            else:
                product_price = product_price - (coupon.amount * item.quantity)
        else:
            product_price = product_price - (coupon.amount * item.quantity)
    
    return product_price 
    

def apply_coupons(items, coupons):
    fixed_products_coupons = coupons.filter(type=Coupon.CouponTypes.FIXED_PRODUCT)
    fixed_basket_coupons = coupons.filter(type=Coupon.CouponTypes.FIXED_BASKET)
    percentage_coupons = coupons.filter(type=Coupon.CouponTypes.PERCENTAGE)
    

    final_price = 0
    for item in items:
        product_price = item.product.sale_price if item.product.sale_price != 0 else item.product.regular_price
        product_price = product_price * item.quantity
        for coupon in fixed_products_coupons:
            product_price = product_discount_price(item, coupon, product_price)
        final_price += product_price

    for coupon in fixed_basket_coupons:
        if coupon.exclude_sale_items and items.exclude(product__sale_price=0).exists():
            raise ValidationError({'detail':"You cannot apply this coupon on items on sale."}) 
        final_price = final_price - coupon.amount
        
    for coupon in percentage_coupons:
        if coupon.exclude_sale_items and items.exclude(product__sale_price=0).exists():
            raise ValidationError({'detail':"You cannot apply this coupon on items on sale."}) 
        final_price = final_price * (1 - (coupon.amount / 100))
    return final_price


@api_view(['POST'])
def verify_new_coupon(request, title):
    
    try:
        coupon = Coupon.objects.get(title=title)
    except:
        raise NotFound("Coupon not found")
    user = request.user
    
    items = get_items(request)

    coupons = request.data['coupons']
    
    return bew(user,coupons, coupon, items)
    

def bew(user, coupons, coupon, items):
    
    items_count = 0
    price = 0


    # included emails
    coupon.user_not_allowed(user)
    
    # repeated use
    coupon.already_used(coupons)
        
    # induvidual use
    coupon.check_individual_use(len(coupons))

    for item in items:
        product = item.product

        # coupon is fixed basket or percentage
        if coupon.is_whole_basket():

            # product is not on sale
            if product.sale_price == 0:
                price = price + (product.regular_price * item.quantity)
            
            # product is on sale
            else:
                if coupon.exclude_sale_items:
                    raise ValidationError({'detail':"You cannot apply this coupon on items on sale."}) 
                else:
                    price = price + (product.sale_price * item.quantity)

        # coupon is fixed product
        else:
            # product is not on sale
            if product.sale_price == 0:
                price = price + ((product.regular_price) * item.quantity)

            # product is on sale
            else:
                price = price + ((product.sale_price) * item.quantity)


        # included products
        coupon.product_not_in_allowed_products(product)

        # excluded products
        coupon.product_in_excluded_products(product)     
        
        # included categories
        coupon.categories_not_in_allowed_categories(product)
            
        # excluded categories
        coupon.categories_in_excluded_categories(product)
            
        items_count = items_count + item.quantity

    
    # expired date
    coupon.check_date()

    # minimum
    coupon.is_lower_than_minimum(price)
    
    # maximum
    coupon.is_over_the_maximum(price)
        
    # coupon usage
    coupon.is_reached_usage_limit()
        
    # limit items
    coupon.is_reached_item_limit(items_count) 
    
    # per person
    coupon.is_reached_per_person_limit(user)
        

    coupons.append(coupon.id)

    coupons = Coupon.objects.filter(id__in=coupons)

    final_price = apply_coupons(items, coupons)

    return Response({'price': final_price, 'coupon': CouponSerial(coupon).data}, status=200)
    
    # sale items


def check_coupons(user,items, coupons):
    items_count = 0
    price = 0

    for item in items:
        product = item.product
        if product.sale_price == 0:
            price = price + (product.regular_price * item.quantity)
        else:
            price = price + (product.sale_price * item.quantity)

        items_count += item.quantity

    # TODO use python's counter to see if there are any duplicate
    # repeated use
    # coupon.already_used(coupons)

    for coupon in coupons:
        # included emails
        coupon.user_not_allowed(user)
            
        # induvidual use
        coupon.check_individual_use(len(coupons) - 1)

        for item in items:
            product = item.product

            # included products
            coupon.product_not_in_allowed_products(product)

            # excluded products
            coupon.product_in_excluded_products(product)     
            
            # included categories
            coupon.categories_not_in_allowed_categories(product)
                
            # excluded categories
            coupon.categories_in_excluded_categories(product)

        # expired date
        coupon.check_date()
            
        # minimum
        coupon.is_lower_than_minimum(price)
        
        # maximum
        coupon.is_over_the_maximum(price)
            
        # coupon usage
        coupon.is_reached_usage_limit()
            
        # limit items
        coupon.is_reached_item_limit(items_count) 
        
        # per person
        coupon.is_reached_per_person_limit(user)

  

@api_view(['POST'])
def verify_coupons(request):
    user = request.user
    coupons_id = request.data['coupons']
    try:
        coupons = Coupon.objects.filter(pk__in=coupons_id)
    except:
        raise NotFound("Coupon not found")
    
    items = get_items(request)

    check_coupons(user,items,coupons)

    final_price = apply_coupons(items, coupons)



    return Response({'price': final_price}, status=200)

def get_items(request):
    user = request.user
    if user.is_authenticated:
        items = user.basket.items.all()
    else:
        items = request.data.get('basket')
        for i, item in enumerate(items):
            items[i] = Item(
                product = Product.objects.get(pk=item['product']),
                quantity = item['quantity'],
            )
    return items