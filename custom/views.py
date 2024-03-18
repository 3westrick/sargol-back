from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from custom.models import Custom
from custom.serial import CustomSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission

# Create your views here.

class CustomListView(generics.ListAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerial
    # authentication_classes = [] # removes all auth methos

    
class CustomRetriveView(generics.RetrieveAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerial
    lookup_field = 'pk'

class CustomCreateView(generics.CreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerial

    def perform_create(self, serializer):
        serializer.save()

class CustomUpdateView(generics.UpdateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerial
    lookup_field = 'pk'

class CustomDeleteView(generics.DestroyAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

