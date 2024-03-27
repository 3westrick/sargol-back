from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from order.models import Order, Item, OrderItem
from order.serial import OrderSerial, ItemSerial

from rest_framework import generics, mixins, permissions, authentication
from rest_framework.exceptions import ValidationError
from base.mixins import CheckPermission, CheckAuth
import time

class ItemListView(CheckAuth, generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

class ItemCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerial

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

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

class OrderListView(CheckAuth,generics.ListAPIView): 
    queryset = Order.objects.all()
    serializer_class = OrderSerial

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()
    

class OrderCreateView(CheckAuth,generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerial

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)