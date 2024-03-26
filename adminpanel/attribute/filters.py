import django_filters
from attribute.models import Attribute

class AttributeFilter(django_filters.FilterSet):
    class Meta:
        model = Attribute
        # fields = ['title']
        fields = {
            'title': ['icontains'],
            # 'release_date': ['exact', 'year__gt'],
        }