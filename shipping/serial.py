from rest_framework import serializers
from shipping.models import Method

class MethodSerial(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = '__all__'