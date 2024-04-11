from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from order.models import Order, Item, OrderItem
from coupon.models import Coupon
from order.serial import OrderSerial, ItemSerial, ItemSerialCreate, ItemListSerial
from rest_framework.exceptions import NotFound

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from base.mixins import CheckAuth

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.pagination import CustomPagePagination, CustomLimitOffsetPagtination
from base.filters import CustomSearch

class ItemListView(CheckAuth, generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerial

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

class ItemCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerialCreate

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')
        if not user.basket.filter(product=product).exists():
            serializer.save(user = user)

class ItemEditView(CheckAuth,generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial
    lookup_field = 'pk'
    
class ItemDeleteView(CheckAuth,generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise ValidationError("Not Authorized")
        return super().perform_destroy(instance)

class OrderListView(CheckAuth, CustomSearch ,generics.ListAPIView): 
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    pagination_class = CustomLimitOffsetPagtination
    search_fields = ['id', 'status']
    ordering_fields = ['id','status']
    pagination_class = CustomPagePagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()
    

class OrderCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

def get_item_count_and_price(items):
    price = 0
    item_counts = 0
    for item in items:
        product = item.product
        if product.sale_price != 0 :
            price += (product.sale_price * item.quantity)
        else:
            price += (product.regular_price * item.quantity)
        item_counts += item.quantity
    return (price, item_counts)


def check_coupons(user,items, coupons,):
    price, item_counts = get_item_count_and_price(items)
    for coupon in coupons:
        if coupon.individual_use and len(coupons) > 1:
            raise ValidationError("The coupon should be used individualy.")
        

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

def get_final_price(items, coupons):
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
    return final_price

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, JWTAuthentication,))
@permission_classes((IsAuthenticated,))
def purchase(request):
    user = request.user
    coupons = request.data['coupons']

    if len(coupons) > 0:
        try:
            coupons = Coupon.objects.filter(pk__in=coupons)
        except:
            raise NotFound("Coupon not found")
        
        items = user.basket.all()

        # print(123)
        check_coupons(user,items,coupons)

        order = user.orders.create()


        final_price = 0
        for item in items:
            product_price = item.product.sale_price if item.product.sale_price != 0 else item.product.regular_price
            product_price = product_price * item.quantity
            for co in coupons:
                product_price = product_discount_price(item, co, product_price)
            final_price += product_price
            order.items.create(product=item.product, quantity=item.quantity, price=product_price)

        for co in coupons:
            if co.type == 'fixed_basket':
                final_price = final_price - co.amount
        
        for co in coupons:
            if co.type == 'percentage':
                final_price = final_price * (1 - (co.amount / 100))

        order.coupons.set(coupons)
        order.price = final_price
        order.save()
        user.basket.all().delete()

    else:
        items = user.basket.all()
        order = user.orders.create()
        for item in items:
            price = item.product.sale_price if item.product.sale_price != 0 else item.product.regular_price
            order.items.create(product=item.product, quantity=item.quantity, price=price)
            
    return Response(status=200)