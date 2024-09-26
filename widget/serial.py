from rest_framework import serializers
from widget.models import Widget, Widgetgroup
from attribute.models import Attribute
from value.models import Value
from category.models import Category

class CategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'slug','image']

class ValueSerial(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ['id', 'title', 'slug']

class AttributeSerial(serializers.ModelSerializer):
    values = ValueSerial(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'slug', 'values']

class WidgetSerial(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id','option', 'value', 'main']

class WidgetGroupSerial(serializers.ModelSerializer):
    # widgets = WidgetSerial(read_only=True, many=True)
    widgets = serializers.SerializerMethodField()
    class Meta:
        model = Widgetgroup
        fields = ['id', 'title','slug', 'widgets']
    
    def get_widgets(self, widgert_group: Widgetgroup):
        return widgert_group.get_widgets()
