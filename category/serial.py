from rest_framework import serializers
from category.models import Category

class InlineCategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'is_active']

class CategorySerial(serializers.ModelSerializer):
    parent_cat = InlineCategorySerial(read_only=True, source='parent')
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'is_active','image', 'parent', 'parent_cat']