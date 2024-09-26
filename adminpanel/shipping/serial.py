from rest_framework import serializers
from shipping.models import Shipping, Zone, Method, ShippingMethod
from base.models import Region

class RegionSerial(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ShippingSerial(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Shipping
        fields = [
            'id',
            'title',
            'slug',
            'description',
            # 'price',
            'product_count'
        ]
        # read_only_fields = ('value',)
    
    def get_product_count(self, shipping):
        return 0

class ShippingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = [
            'id',
            'title',
            'slug',
        ]
    

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['name', 'regions', 'wildcard']

class MethodSerializer(serializers.ModelSerializer):

    shipping_classes = serializers.SerializerMethodField(read_only=True)
    local_pickup_cost = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Method
        fields = '__all__'

    def get_local_pickup_cost(self,method):
        if method.type == 'local_pickup':
            return f'{method.local_pickup_cost}*' if method.local_pickup_qty else method.local_pickup_cost
        return None
    def get_shipping_classes(self, method):
        if method.type == 'flat_rate':
            query = method.classes.all()
            data = {}
            for q in query:
                data[q.shipping_class.id] = f'{q.cost}*' if q.cost_qty else q.cost
            
            return data
            # return data
        return None

class ZoneListSerializer(serializers.ModelSerializer):
    class InlineMethodSerializer(serializers.ModelSerializer):
        class Meta:
            model = Method
            fields = ['name']

    methods = InlineMethodSerializer(many=True)
    regions = RegionSerial(many=True)
    class Meta:
        model = Zone
        fields = '__all__'

class ZoneSingleSerializer(serializers.ModelSerializer):
    methods = MethodSerializer(many=True)
    regions = RegionSerial(many=True)
    class Meta:
        model = Zone
        fields = '__all__'