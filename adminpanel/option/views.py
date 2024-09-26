from django.shortcuts import render
from shipping.models import Shipping, ShippingMethod, Zone, Method
from adminpanel.shipping.serial import ShippingSerial, ZoneSerializer, MethodSerializer, ZoneListSerializer, ZoneSingleSerializer
from base.models import Region
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission, ModelPermission
from option.models import Option
from adminpanel.option.serial import OptionSerial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch


class ShippingOptionsList(CheckPermission, generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        # 'shipping_calculations',
        'shipping_destination',
        ])
    serializer_class = OptionSerial

class ShippingOptionsUpdate(CheckPermission, generics.UpdateAPIView):
    titles = [
        # 'shipping_calculations',
        'shipping_destination',
        ]
    queryset = Option.objects.filter(title__in= titles)
    serializer_class = OptionSerial

    def update(self, request, *args, **kwargs):
        for title in self.titles:
            instance = self.queryset.get(title=title)
            instance.value = request.data.get(title)
            instance.save()
        return Response(status=status.HTTP_200_OK)
        


class TaxOptionsList(CheckPermission, generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        'price_entered_with_tax',
        'display_prices_in_the_shop',
        'display_prices_during_basket_and_checkout',
        ])
    serializer_class = OptionSerial

class TaxOptionsUpdate(CheckPermission, generics.UpdateAPIView):
    titles = [
        'price_entered_with_tax',
        'display_prices_in_the_shop',
        'display_prices_during_basket_and_checkout',
    ]
    queryset = Option.objects.filter(title__in= titles)
    serializer_class = OptionSerial

    def update(self, request, *args, **kwargs):
        for title in self.titles:
            instance = self.queryset.get(title=title)
            instance.value = request.data.get(title)
            instance.save()
        return Response(status=status.HTTP_200_OK)
        


class GeneralOptionsList(CheckPermission, generics.ListAPIView):
    queryset = Option.objects.filter(title__in= [
        'selling_locations',
        'specific_countries',
        'exception_countries',
        'shipping_locations',
        'shipping_countries',
        ])
    serializer_class = OptionSerial

class GeneralOptionsUpdate(CheckPermission, generics.UpdateAPIView):
    titles = [
        'selling_locations',
        'specific_countries',
        'exception_countries',
        'shipping_locations',
        'shipping_countries',
        ]
    queryset = Option.objects.filter(title__in= titles)
    serializer_class = OptionSerial

    def update(self, request, *args, **kwargs):
        for title in self.titles:
            instance = self.queryset.get(title=title)
            instance.value = request.data.get(title)
            instance.save()
        return Response(status=status.HTTP_200_OK)
        
