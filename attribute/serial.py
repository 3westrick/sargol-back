from rest_framework import serializers
from attribute.models import Attribute
from value.models import Value

class InlineValueSerial(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ['id','title', 'slug']

class AttributeSerial(serializers.ModelSerializer):
    values = InlineValueSerial(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ['id','title','slug' ,'values']
