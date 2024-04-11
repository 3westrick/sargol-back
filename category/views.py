from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from category.models import Category
from category.serial import CategorySerial
from product.models import Product
from product.serial import ProductSerialList

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission
from base.pagination import CustomPagePagination
from base.filters import CustomSearch, CustomFilter
import time
from django.db.models import Q

# Create your views here.

class CategoryListView(CustomSearch, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerial
    pagination_class = CustomPagePagination
    search_fields = ['id', 'title', 'slug']
    ordering_fields = ['id','title']

    
class CategoryRetriveView(CustomFilter, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialList
    pagination_class = CustomPagePagination
    search_fields = ['id', 'title', 'description']
    ordering_fields = ['id','title', 'slug', 'regular_price']
    # filterset_class = ProductFilter
    filterset_fields = {
        "tax_status": ["exact"],
        'tax_class': ['exact'],
        'stock_management': ['exact'],
        'stock_status': ['exact'],

        'sold_individually': ['exact'],
        'unit': ['icontains'],
        'shipping_class': ['exact'],

        'attributes__attribute__slug': ['in'], # attributes__attribute__slug__in=color,size
        'categories__slug': ['in'], # categories__slug__in=cat-1,cat-2

        'regular_price': ['gte', 'lte'] # regular_price__gte=100&regular_price__lte=
    }

    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        self.queryset = Product.objects.filter(Q(categories__slug=category_slug) & Q(parent=None))
        return super().get_queryset()

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

