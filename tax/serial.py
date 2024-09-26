from tax.models import Tax, Rate
from rest_framework import serializers

class RateSerial(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = [
            "id",
            "country",
            "states",
            "zip_code",
            "name",
            "rate",
            "on_shipping",
        ]

class TaxSerial(serializers.ModelSerializer):
    rates = RateSerial(many=True)
    class Meta:
        model = Tax
        fields = '__all__'