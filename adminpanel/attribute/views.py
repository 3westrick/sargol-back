from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from attribute.models import Attribute
from adminpanel.attribute.serial import AttributeSerial

from rest_framework import generics
from base.mixins import CheckPermission
from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch
from adminpanel.attribute.filters import AttributeFilter
# Create your views here.

class AttributeListView(CheckPermission, CustomSearch,generics.ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    pagination_class = CustomLimitOffsetPagtination
    search_fields = ['title', 'slug', 'values__title']
    ordering_fields = ['id','title', 'slug', 'type']

    # authentication_classes = [] # removes all auth methos
    # permission_classes = []


    
class AttributeRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    lookup_field = 'pk'

class AttributeCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial

    def perform_create(self, serializer):
        serializer.save()

class AttributeUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()

class AttributeDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

