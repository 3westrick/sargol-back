from django.shortcuts import render
from product.models import Product
from adminpanel.product.serial import ProductSerial, ProductSecondSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission
import time
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.

class ProductListView(CheckPermission, generics.ListAPIView):
    queryset = Product.objects.filter(parent=None)
    serializer_class = ProductSerial


    
class ProductRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial
    lookup_field = 'pk'

@api_view(['POST'])
def create_product(request):
    obj = {}
    for key in request.data:
        # if key == 'categories':
        #     obj['categories'] = request.data.getlist(key)
        # elif key == 'attributes':
        #     obj['attributes'] = request.data.getlist(key)
        # elif key == 'values':
        #     obj['values'] = request.data.getlist(key)
        # elif key == 'gallery':
        #     obj['gallery'] = request.data.getlist(key)
        # elif key == 'visibleAttributes':
        #     obj['visibleAttributes'] = request.data.getlist(key)
        # elif key == 'variantAttributes':
        #     obj['variantAttributes'] = request.data.getlist(key)
        # else:
        #     obj[key] = request.data[key]
        obj[key] = request.data[key]
    obj['categories'] = request.data.getlist('categories', [])
    obj['attributes'] = request.data.getlist('attributes', [])
    obj['values'] = request.data.getlist('values', [])
    obj['gallery'] = request.data.getlist('gallery', [])
    obj['visibleAttributes'] = request.data.getlist('visibleAttributes', [])
    obj['variantAttributes'] = request.data.getlist('variantAttributes', [])
    
    # for key, value in obj.items():
    #     print(key, value)

    print(obj['variantAttributes'])
    serial_product = ProductSerial(data=obj)
    print(serial_product.is_valid(raise_exception=True))
    print(dir(serial_product.validated_data))
    
    # if serial_product.is_valid(raise_exception=True):
    #     serial_product.save()
    return Response(status=status.HTTP_201_CREATED)

class ProductCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial


class ProductUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSecondSerial
    lookup_field = 'pk'


class ProductDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

