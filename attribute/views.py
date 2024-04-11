from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from attribute.models import Attribute
from attribute.serial import AttributeSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission
from base.filters import CustomFilter

# Create your views here.

class AttributeListView(CheckPermission,CustomFilter , generics.ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    filterset_fields = {
        "id": ["in"],
    }
    # authentication_classes = [] # removes all auth methos

    
class AttributeRetriveView(generics.RetrieveAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    lookup_field = 'pk'

class AttributeCreateView(generics.CreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial

    def perform_create(self, serializer):
        serializer.save()

class AttributeUpdateView(generics.UpdateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()

class AttributeDeleteView(generics.DestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

