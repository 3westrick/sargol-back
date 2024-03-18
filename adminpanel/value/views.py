from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from value.models import Value
from adminpanel.value.serial import ValueSerial, ValueAttributeSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission

# Create your views here.

class ValueListView(CheckPermission, generics.ListAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueAttributeSerial
    # authentication_classes = [] # removes all auth methos

    
class ValueRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueAttributeSerial
    lookup_field = 'pk'

class ValueCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueAttributeSerial

    def perform_create(self, serializer):
        serializer.save()

class ValueUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueSerial
    lookup_field = 'pk'

class ValueDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

