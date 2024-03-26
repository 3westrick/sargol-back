import django_filters
from product.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # fields = ['title']
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'short_description': ['icontains'],
        }