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
    


def get_price(coupon, coupons, items):
    coupons = Coupon.objects.filter(pk__in=coupons)
    final_price = 0
    for item in items:
        product_price = item.product.sale_price if item.product.sale_price != 0 else item.product.regular_price
        product_price = product_price * item.quantity
        product_price = product_discount_price(item, coupon, product_price)
        for co in coupons:
            product_price = product_discount_price(item, coupon, product_price)
        final_price += product_price
    
    if coupon.type == 'fixed_basket':
        final_price = final_price - coupon.amount
    
    for co in coupons:
        if co.type == 'fixed_basket':
            final_price = final_price - co.amount

    if coupon.type == 'percentage':
        final_price = final_price * (1 - (coupon.amount / 100))
    
    for co in coupons:
        if co.type == 'percentage':
            final_price = final_price * (1 - (co.amount / 100))

    return final_price
    


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, JWTAuthentication,))
@permission_classes((IsAuthenticated,))
def verify_new_coupon(request, title):
    try:
        coupon = Coupon.objects.get(title=title)
    except:
        raise NotFound("Coupon not found")
    
    user = request.user

    if coupon.allowed_users.count() > 0:
        if not coupon.allowed_users.filter(pk=user.id).exists():
            raise ValidationError(f"This user can't use this couopn.")

    if not coupon.usage_limit > 0 and coupon.usage_limit != -1:
        raise ValidationError(f"Coupon usage has reached its limit usage.")
        
    if coupon.user_used.filter(pk=user.id).count() > coupon.user_limit and coupon.user_limit != -1:
        raise ValidationError(f"User usage limit reached.")
    

    price = 0
    p = []
    ep = []
    c = []
    ec = []
    item_counts = 0
    items = user.basket.all()
    for item in items:
        product = item.product
        if product.sale_price != 0 :
            price += (product.sale_price * item.quantity)
        else:
            price += (product.regular_price * item.quantity)

        if coupon.products.count() != 0:
            if not coupon.products.filter(pk=product.pk).exists():
                p.append(product.pk)
        if coupon.exclude_products.count() != 0:
            if coupon.exclude_products.filter(pk=product.pk).exists():
                ep.append(product.pk)


        if coupon.categories.count() != 0:
            for cate in product.categories.all():
                if not coupon.categories.filter(pk=cate.pk).exists():
                    c.append(product.pk)

        if coupon.exclude_categories.count() != 0:
            for cate in product.categories.all():
                if coupon.exclude_categories.filter(pk=cate.pk).exists():
                    ec.append(product.pk)
        
        item_counts += item.quantity

    if coupon.item_limit != -1 and coupon.item_limit < item_counts:
        raise ValidationError(f"Item limit reached")

    if len(p) > 0:
        raise ValidationError(f"These products can't be in list")
    
    if len(ep) > 0:
        raise ValidationError(f"These products can't be in list")
    
    if len(c) > 0:
        raise ValidationError(f"These categories can't be in list")
    
    if len(ec) > 0:
        raise ValidationError(f"These categories can't be in list")
        
    
    if coupon.minimum != -1 and price < coupon.minimum:
        raise ValidationError("The price is lower than limit.")
    if coupon.maximum != -1 and price > coupon.maximum:
        raise ValidationError("The price is over the limit.")
    
    coupons = request.data['coupons']
    for temp_coupon in coupons:
        try:
            tp = Coupon.objects.get(pk=temp_coupon)
        except:
            raise NotFound("Coupon not found")
        if coupon.individual_use or tp.individual_use:
            raise ValidationError("The coupon should be used individualy.")
        if coupon == tp:
            raise ValidationError("Coupon already in use.")
    
    price = get_price(coupon, coupons, items)
        
    return Response({'price': price, 'coupon': CouponSerial(coupon).data}, status=200)

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, JWTAuthentication,))
@permission_classes((IsAuthenticated,))
def verify_coupons(request):
    user = request.user
    coupons = request.data['coupons']
    try:
        coupons = Coupon.objects.filter(pk__in=coupons)
    except:
        raise NotFound("Coupon not found")
    price = 0
    items = user.basket.all()
    item_counts = 0
    for item in items:
        product = item.product
        if product.sale_price != 0 :
            price += (product.sale_price * item.quantity)
        else:
            price += (product.regular_price * item.quantity)
        item_counts += item.quantity

    # use python's counter to see if there are any duplicate
    for coupon in coupons:
        
        if coupon.individual_use and len(coupons) > 1:
            raise ValidationError("The coupon should be used individualy.")
        
        # use python counter
        if coupon.allowed_users.count() > 0:
            if not coupon.allowed_users.filter(pk=user.id).exists():
                raise ValidationError(f"This user can't use this couopn.")

        if coupon.usage_limit != -1 and not coupon.usage_limit > 0:
            raise ValidationError(f"Coupon usage has reached its limit usage.")
        if coupon.user_limit != -1 and coupon.user_used.filter(pk=user.id).count() > coupon.user_limit:
            raise ValidationError(f"User usage limit reached.")
        if coupon.item_limit != -1 and coupon.item_limit < item_counts:
            raise ValidationError(f"Item limit reached")
        if coupon.minimum != -1 and price < coupon.minimum:
            raise ValidationError("The price is lower than limit.")
        if coupon.maximum != -1 and price > coupon.maximum:
            raise ValidationError("The price is over the limit.")
        
        p = []
        ep = []
        c = []
        ec = []
        for item in items:
            product = item.product
            if coupon.products.count() != 0:
                if not coupon.products.filter(pk=product.pk).exists():
                    p.append(product.pk)

            if coupon.exclude_products.count() != 0:
                if coupon.exclude_products.filter(pk=product.pk).exists():
                    ep.append(product.pk)

            if coupon.categories.count() != 0:
                for cate in product.categories.all():
                    if not coupon.categories.filter(pk=cate.pk).exists():
                        c.append(coupon.pk)

            if coupon.exclude_categories.count() != 0:
                for cate in product.categories.all():
                    if coupon.exclude_categories.filter(pk=cate.pk).exists():
                        ec.append(product.pk)
        if len(p) > 0:
            raise ValidationError(f"These products can't be in list")
    
        if len(ep) > 0:
            raise ValidationError(f"These products can't be in list")
    
        if len(c) > 0:
            raise ValidationError(f"These categories can't be in list")
    
        if len(ec) > 0:
            raise ValidationError(f"These categories can't be in list")
        
    final_price = 0
    for item in items:
        product_price = item.product.sale_price if item.product.sale_price != 0 else item.product.regular_price
        product_price = product_price * item.quantity
        for co in coupons:
            product_price = product_discount_price(item, co, product_price)
        final_price += product_price

    for co in coupons:
        if co.type == 'fixed_basket':
            final_price = final_price - co.amount
    
    for co in coupons:
        if co.type == 'percentage':
            final_price = final_price * (1 - (co.amount / 100))

    return Response({'price': final_price}, status=200)