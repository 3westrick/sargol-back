from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shipping.models import Shipping, Zone
from option.models import Option
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from shipping.serial import MethodSerial
from order.models import Item
from product.models import Product
from coupon.models import Coupon

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, JWTAuthentication,))
def index(request):
    # TODO: check country
    selling_locations = Option.objects.get(title = 'selling_locations').value
    specific_countries = Option.objects.get(title = 'specific_countries').value
    exception_countries = Option.objects.get(title = 'exception_countries').value
    shipping_locations = Option.objects.get(title = 'shipping_locations').value
    shipping_countries = Option.objects.get(title = 'shipping_countries').value

    country = request.data.get('country')
    postcode = request.data.get('postcode')

    if country is None or country == '':
        return Response("")
        # raise ValidationError({'error': 'please select a country'})
    if postcode is None or postcode == '':
        return Response("")
        # raise ValidationError({'error': 'please select a postcode'})
    
    basket = get_items(request)
    
    # for item in basket:
    #     print(item.product)
    prices = []
    if selling_locations == 'all_countries':
        if shipping_locations == 'ship_to_all_countries_you_sell_to' or shipping_locations == 'ship_to_all_countries':
            # any country would be ok
            # TODO: calculate shipping price
            for zone in Zone.objects.all():
                if zone.valid_country(country) and zone.valid_zip(postcode):
                    for method in zone.methods.filter(enabled=True):
                        shipping_price = method.check_products(basket, auth=request.user.is_authenticated)
                        if shipping_price:
                            m = MethodSerial(instance=method).data
                            m['add_price'] = shipping_price
                            prices.append(m)
        if shipping_locations == 'deliver_to_specific_countries':
            if country in shipping_countries.split(';'):
                # TODO: check zip
                # TODO: calculate shipping price
                pass
            else:
                raise ValidationError({'error': 'there is no shipping to your country'})



    elif selling_locations == 'all_countries_except_for':
        pass
    else:
        if shipping_locations == 'ship_to_all_countries_you_sell_to' or shipping_locations == 'ship_to_all_countries':
            print(specific_countries.split(';'))
        elif shipping_locations == 'deliver_to_specific_countries': 
            print(specific_countries.split(';'))
            print(shipping_countries.split(';'))



    # TODO: get zones with the same country
    # TODO: check if zip is not None and is valid for zone
    return Response(prices)

def get_items(request):
    user = request.user
    if user.is_authenticated:
        basket = user.basket
    else:
        basket = {}
        basket['items'] = request.data.get('basket')
        basket['coupons'] = Coupon.objects.filter(id__in=request.data.get('coupons'))
        basket['final_price'] = request.data.get('final_price')
        basket['discounted_price'] = request.data.get('discounted_price')
        for i, item in enumerate(basket['items']):
            basket['items'][i] = Item(
                product = Product.objects.get(pk=item['product']),
                quantity = item['quantity'],
            )
    return basket