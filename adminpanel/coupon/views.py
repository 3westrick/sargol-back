from django.shortcuts import render
from coupon.models import Coupon
from adminpanel.coupon.serial import CouponSerial, CouponSingleSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.pagination import ModelPaginateAndFilterSecond

class CouponListView(CheckPermission, ModelPaginateAndFilterSecond, generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerial
    search_fields = ['id', 'title', 'description']
    ordering_fields = ['id','title', ]


class CouponRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSingleSerial
    lookup_field = 'pk'

class CouponCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerial
    # datetime.fromtimestamp(1711050808346/1000)


class CouponUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerial
    lookup_field = 'pk'


class CouponDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerial
    lookup_field = 'pk'