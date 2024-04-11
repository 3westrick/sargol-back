from rest_framework.filters import  OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class CustomSearch():
    filter_backends = [SearchFilter, OrderingFilter, ]


# if using this, add filterset_class = ProductFilter
"""
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # fields = ['title']
        fields = {
            'tax_status': ['exact'],
            'tax_class': ['exact'],
            'stock_management': ['exact'],
            'stock_status': ['exact'],

            'sold_individually': ['exact'],
            'unit': ['icontains'],
            'shipping_class': ['exact'],
        }
"""

# or filterset_fields
"""
filterset_fields = {
        "tax_status": ["exact"],
    }
"""
class CustomFilter():
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter, ]