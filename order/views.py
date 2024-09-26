from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from order.models import Order, Item, OrderItem, Basket
from coupon.models import Coupon
from order.serial import OrderSerial, ItemSerial, ItemSerialCreate, ItemListSerial,BasketSerial
from rest_framework.exceptions import NotFound
from coupon.views import apply_coupons
from product.models import Product

from shipping.models import Method

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
        user = self.request.user
        try:
            basket = user.basket
        except:
            basket = Basket.objects.create(user=user)
        self.queryset = self.queryset.filter(basket=basket)
        return super().get_queryset()

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication, JWTAuthentication])
def create_basket(request):
    user = request.user
    coupons_id = request.data['coupons']
    coupons = Coupon.objects.filter(pk__in=coupons_id)
    try:
        basket = user.basket
        basket.items.all().delete()
    except:
        basket = Basket.objects.create(user=user)
        basket.coupons.delete()
    items = request.data.get('basket')
    for item in items:
        serializer = ItemSerialCreate(data=item)
        serializer.is_valid(raise_exception=True)
        serializer.save(basket = basket)
    
    items = basket.items.all()
    check_coupons(user,items,coupons)
    basket.update_price()
    discounted_price = apply_coupons(items, coupons)
    basket.discounted_price = discounted_price
    basket.coupons.set(coupons)
    basket.save()
    return Response("ok")

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication, JWTAuthentication])
def update_basket(request):
    user = request.user
    coupons_id = request.data['coupons']
    coupons = Coupon.objects.filter(pk__in=coupons_id)
    basket = user.basket
    items = basket.items.all()
    check_coupons(user,items,coupons)
    basket.update_price()
    discounted_price = apply_coupons(items, coupons)
    basket.discounted_price = discounted_price
    basket.coupons.set(coupons)
    basket.save()
    return Response(f"ok {discounted_price}")

class BasketView(CheckAuth, generics.RetrieveAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerial

    def get_object(self):
        return self.request.user.basket


class BasketUpdateView(CheckAuth, generics.UpdateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerial

    def get_object(self):
        return self.request.user.basket
    
    def perform_update(self, serializer):
        basket = serializer.save()
        basket.update_price()
    
class ItemCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerialCreate

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')
        try:
            basket = user.basket
        except:
            basket = Basket.objects.create(user=user)
            
        if not user.basket.items.filter(product=product).exists():
            serializer.save(basket = basket)
            

class ItemEditView(CheckAuth,generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial
    lookup_field = 'pk'
    
class ItemDeleteView(CheckAuth,generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if self.request.user != instance.basket.user:
            raise ValidationError("Not Authorized")
        return super().perform_destroy(instance)

class OrderListView(CheckAuth, CustomSearch ,generics.ListAPIView): 
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    # pagination_class = CustomLimitOffsetPagtination
    search_fields = ['id', 'status']
    ordering_fields = ['id','status']
    # pagination_class = CustomPagePagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
        # self.queryset = self.queryset.filter(user=self.request.user)
        # return super().get_queryset()
    

class OrderCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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

        
def product_discount_price(item, coupon, product_price):
    if item.product.sale_price != 0:
        if coupon.exclude_sale_items:
            pass
        else:
            product_price = product_price - (coupon.amount * item.quantity)
    else:
        product_price = product_price - (coupon.amount * item.quantity)
    
    return product_price 




@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, JWTAuthentication,))
@permission_classes((IsAuthenticated,))
def purchase(request):
    user = request.user
    try:
        method = Method.objects.get(pk = request.data.get("method"))
    except:
        raise ValidationError('not found')
    coupons = user.basket.coupons.all()
    final_price = user.basket.final_price
    shipping_price = method.check_products(user.basket)
    discounted_price = user.basket.discounted_price
    reduced_price = final_price - discounted_price

    print("Items subtotal",final_price)
    print("Shipping price",shipping_price)
    print("Order total", shipping_price + final_price)
    print("Discount", reduced_price)
    print("Paid:", shipping_price + final_price - reduced_price)

    # if method.check_products(user.basket) == request.data.get("add_price"):
    
    #     return Response("")
    # else:
    #     raise ValidationError("Sth wrong")
    
    ip = get_client_ip(request)

    first_name = request.data.get('first_name')
    if first_name is None or first_name == '': raise ValidationError('First name is required.')
    
    last_name = request.data.get('last_name')
    if last_name is None or last_name == '': raise ValidationError('Last name is required.')

    email = request.data.get('email')
    if email is None or email == '': raise ValidationError('Email is required.')

    country = request.data.get('country')
    if country is None or country == '': raise ValidationError('Country is required.')

    city = request.data.get('city')
    if city is None or city == '': raise ValidationError('Town is required.')

    address = request.data.get('address')
    if address is None or address == '': raise ValidationError('Address is required.')

    postcode = request.data.get('postcode')
    if postcode is None or postcode == '': raise ValidationError('Post code is required.')

    phone = request.data.get('phone')
    if phone is None or phone == '': raise ValidationError('Phone is required.')
        


    if len(coupons) > 0:
        # try:
        #     coupons = Coupon.objects.filter(pk__in=coupons)
        # except:
        #     raise NotFound("Coupon not found")

        items = user.basket.items.all()

        check_coupons(user,items,coupons)

        order = Order.objects.create(
            user=user,
            phone=phone,
            country=country,
            city=city,
            postcode=postcode,
            address=address,
            email=email,
            name=f'{first_name} {last_name}',
            ip=ip,
            subtotal = final_price,
            shipping_price = shipping_price,
            discounted_price = discounted_price
        )

        order.coupons.set(coupons)

    else:
        items = user.basket.items.all()
        order = Order.objects.create(
            user=user,
            phone=phone,
            country=country,
            city=city,
            postcode=postcode,
            address=address,
            email=email,
            name=f'{first_name} {last_name}',
            ip=ip,
            subtotal = final_price,
            shipping_price = shipping_price,
        )

    for item in items:
        product = item.product
        product.check_individually(item.quantity)
        on_backorder, notify = product.check_stock(item.quantity)

        price = product.sale_price if product.sale_price != 0 else product.regular_price
        price = price * item.quantity
        order.items.create(product=product, quantity=item.quantity, price=price, backorder=on_backorder,notify=notify )

    order.save()
    user.basket.items.all().delete()

    return Response(status=200)