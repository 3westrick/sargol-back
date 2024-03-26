from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from category.models import Category
from adminpanel.category.serial import CategorySerial, CategoryProductSerial
# from django_filters import rest_framework as filters
from rest_framework import generics
from base.mixins import CheckPermission
# from adminpanel.category.filters import CategoryFilter
from base.pagination import ModelPaginateAndFilter
# Create your views here.

class CategoryListView(CheckPermission, ModelPaginateAndFilter,generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial
    search_fields = ['title', 'slug']
    ordering_fields = ['id','title', 'slug', 'parent']

    
class CategoryProductListView(CheckPermission,generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryProductSerial

    
class CategoryRetriveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial
    lookup_field = 'pk'

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial
    lookup_field = 'pk'


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

