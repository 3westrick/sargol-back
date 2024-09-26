from django.shortcuts import render
from rest_framework.decorators import api_view
from option.models import Option
from .serial import OptionSerial
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.
class ShippingOptionsList(generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        'shipping_calculations',
        'shipping_destination',
        ])
    serializer_class = OptionSerial

class TaxOptionsList(generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        'price_entered_with_tax',
        'display_prices_in_the_shop',
        'display_prices_during_basket_and_checkout',
        ])
    serializer_class = OptionSerial

class GeneralOptionsList(generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        'selling_locations',
        'specific_countries',
        'exception_countries',
        'shipping_locations',
        'shipping_countries',
        ])
    serializer_class = OptionSerial