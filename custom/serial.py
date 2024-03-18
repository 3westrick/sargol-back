from rest_framework import serializers
from custom.models import Custom
from attribute.models import Attribute


class CustomAttributeSerial(serializers.ModelSerializer):
    class Meta:
        model= Custom
        fields = ['id','title','slug', 'attribute', 'image','color']

class CustomSerial(serializers.ModelSerializer):
    class Meta:
        model= Custom
        fields = ['id','title', 'image']

