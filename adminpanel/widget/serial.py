from rest_framework import serializers
from widget.models import Widget, WidgetGroup
from attribute.models import Attribute
from value.models import Value

class ValueSerial(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ['id', 'title', 'slug']

class AttributeSerial(serializers.ModelSerializer):
    values = ValueSerial(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'slug', 'values']


class WidgetCreateSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'title', 'group', 'type', 'attribute', 'display' ]

class WidgetUpdateSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'title', 'attribute', 'display' ]

class WidgetSerial(serializers.ModelSerializer):
    attribute = AttributeSerial(read_only=True)
    class Meta:
        model = Widget
        fields = ['id', 'title', 'group', 'type', 'attribute', 'display']

class WidgetGroupSerial(serializers.ModelSerializer):
    widgets = WidgetSerial(many=True, read_only=True)
    class Meta:
        model = WidgetGroup
        fields = ['id', 'type', 'widgets']

