from django.shortcuts import render
from tax.models import Tax, Rate
from adminpanel.tax.serial import TaxSerial, TaxSingleSerial, RateListSerial, RateCreateSerial

from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch, CustomFilter
import django_filters

class TaxListView(CheckPermission, CustomSearch, generics.ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial
    pagination_class = CustomLimitOffsetPagtination 
    search_fields = ['id', 'title']
    ordering_fields = ['id','title', ]

class TaxAllListView(CheckPermission, generics.ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial

class TaxRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSingleSerial
    lookup_field = 'pk'

class TaxCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial


class TaxUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial
    lookup_field = 'pk'


class TaxDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial
    lookup_field = 'pk'


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'tax__id': ['exact'],
        }

class RateListView(CheckPermission, CustomFilter, generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateListSerial
    filterset_class = RateFilter

class RateCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateCreateSerial

class RateUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateCreateSerial
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except Exception as e:
            print(e)
        return Response('')