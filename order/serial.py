from order.models import Order, Item
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ItemSerial(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'created_at', 'edited_at']

    def update(self, instance, validated_data):
        if instance.user != self.context.get('request').user:
            raise ValidationError("Not Authorised")
        return super().update(instance, validated_data)

class OrderSerial(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'items',]
