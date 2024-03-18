from rest_framework import serializers
from value.models import Value
from attribute.models import Attribute


class ValueAttributeSerial(serializers.ModelSerializer):
    class Meta:
        model= Value
        fields = ['id','title', 'attribute']

class ValueSerial(serializers.ModelSerializer):
    class Meta:
        model= Value
        fields = ['id','title']
