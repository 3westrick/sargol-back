from django.shortcuts import render
from shipping.models import Shipping, ShippingMethod, Zone, Method
from adminpanel.shipping.serial import ShippingSerial, ZoneSerializer, MethodSerializer, ZoneListSerializer, RegionSerial
from base.models import Region
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission, ModelPermission


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch


class RegionListView(CheckPermission, generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerial