from rest_framework import serializers
from tax.models import Tax, Rate

class TaxSerial(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = [
            'id',
            'title',
        ]

class RateListSerial(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = [
            'id',
            'country',
            'states',
            'zip_code',
            # 'cities',
            'rate',
            'name',
            'on_shipping',
        ]

class RateCreateSerial(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = [
            'id',
            'tax',
            'country',
            'states',
            'zip_code',
            # 'cities',
            'rate',
            'name',
            'on_shipping',
        ]

class TaxSingleSerial(serializers.ModelSerializer):
    rates = RateListSerial(many=True)
    class Meta:
        model = Tax
        fields = [
            'id',
            'title',
            'rates'
        ]
