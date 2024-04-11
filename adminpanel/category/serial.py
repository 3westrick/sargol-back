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
        
    def update(self, instance, validated_data):
        if validated_data.get('image', None) == None:
            validated_data['image'] = instance.image
        return super().update(instance, validated_data)

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