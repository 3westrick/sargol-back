import django_filters
from category.models import Category

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        # fields = ['title']
        fields = {
            'title': ['icontains'],
            # 'release_date': ['exact', 'year__gt'],
        }