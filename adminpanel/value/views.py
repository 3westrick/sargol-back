from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from value.models import Value
from adminpanel.value.serial import ValueSerial, ValueAttributeSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission
from base.pagination import ModelPaginateAndFilter, ModelPaginateAndFilterSecond
import django_filters


# Create your views here.

class ValueFilter(django_filters.FilterSet):
    class Meta:
        model = Value
        # fields = ['title']
        fields = {
            'attribute__id': ['exact'],
        }

class ValueListView(CheckPermission, ModelPaginateAndFilterSecond,generics.ListAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueAttributeSerial
    search_fields = ['title', 'slug']
    ordering_fields = ['id','title','slug']
    filterset_class = ValueFilter

    
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

@api_view(['PUT'])
def update_value(request, pk):
    print(request.data)
    return Response(status=200)

class ValueDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueSerial
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()

