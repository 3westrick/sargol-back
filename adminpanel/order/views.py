from django.shortcuts import render
from coupon.models import Coupon
from order.models import Order
from adminpanel.order.serial import OrderSerial, OrderSingleSerial

from rest_framework import generics
from base.mixins import CheckPermission

from rest_framework.response import Response
from rest_framework import status

from base.pagination import ModelPaginateAndFilterSecond

class OrderListView(CheckPermission, ModelPaginateAndFilterSecond, generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    search_fields = ['id', 'status']
    ordering_fields = ['id','status']


class OrderRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSingleSerial
    lookup_field = 'pk'

class OrderCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    # datetime.fromtimestamp(1711050808346/1000)


class OrderUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    lookup_field = 'pk'


class OrderDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial
    lookup_field = 'pk'