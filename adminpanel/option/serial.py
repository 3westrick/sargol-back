from option.models import Option
from rest_framework import serializers

class OptionSerial(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'