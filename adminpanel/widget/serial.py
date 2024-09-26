from rest_framework import serializers
from widget.models import Widget, Widgetgroup
from attribute.models import Attribute
from value.models import Value


class WidgetCreateSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['option', 'value',]

class WidgetUpdateSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'value',]

class WidgetSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'option', 'value','main']

class WidgetGroupSerial(serializers.ModelSerializer):
    widgets = WidgetSerial(many=True, read_only=True)
    class Meta:
        model = Widgetgroup
        fields = ['id','title', 'slug' ,'widgets']

