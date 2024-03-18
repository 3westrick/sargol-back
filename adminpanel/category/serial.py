from rest_framework import serializers
from category.models import Category

class InlineCategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'slug', 'is_active']

class CategorySerial(serializers.ModelSerializer):
    parent_cat = InlineCategorySerial(read_only=True, source='parent')
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug','image', 'is_active', 'parent', 'parent_cat']

class CategoryProductSerial(serializers.ModelSerializer):
    parent_cat = InlineCategorySerial(read_only=True, source='parent')
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug','image', 'is_active', 'parent', 'parent_cat', 'children']

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj).order_by('title')
        serializer = CategoryProductSerial(children, many=True)
        return serializer.data