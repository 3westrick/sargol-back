from rest_framework import serializers
from value.models import Value
from attribute.models import Attribute


class ValueAttributeSerial(serializers.ModelSerializer):
    class Meta:
        model= Value
        fields = ['id','title','slug', 'attribute', 'image','color']

class ValueSerial(serializers.ModelSerializer):
    class Meta:
        model= Value
        fields = ['id','title', 'slug', 'image','color']
    
    def update(self, instance, validated_data):
        print(validated_data.get('image'))
        if validated_data.get('image', None) == None:
            validated_data['image'] = instance.image
        return super().update(instance, validated_data)
