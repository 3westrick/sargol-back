from django.shortcuts import render
from shipping.models import Shipping, ShippingMethod, Zone, Method
from adminpanel.shipping.serial import ShippingSerial, ZoneSerializer, MethodSerializer, ZoneListSerializer, ZoneSingleSerializer
from base.models import Region
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, mixins, permissions, authentication
from base.mixins import CheckPermission, ModelPermission


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch

class ShippingListView(CheckPermission, CustomSearch, generics.ListAPIView):
    queryset = Shipping.objects.exclude(slug='no-shipping-class')
    serializer_class = ShippingSerial
    pagination_class = CustomLimitOffsetPagtination 
    search_fields = ['id', 'title']
    ordering_fields = ['id','title', ]

class ShippingAllListView(CheckPermission, generics.ListAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerial

class ShippingRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Shipping.objects.exclude(slug='no-shipping-class')
    serializer_class = ShippingSerial
    lookup_field = 'pk'

class ShippingCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Shipping.objects.exclude(slug='no-shipping-class')
    serializer_class = ShippingSerial
    # datetime.fromtimestamp(1711050808346/1000)


class ShippingUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Shipping.objects.exclude(slug='no-shipping-class')
    serializer_class = ShippingSerial
    lookup_field = 'pk'


class ShippingDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Shipping.objects.exclude(slug='no-shipping-class')
    serializer_class = ShippingSerial
    lookup_field = 'pk'


class ZoneListView(CheckPermission, generics.ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneListSerializer

class ZoneRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSingleSerializer

class ZoneCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def create(self, request, *args, **kwargs):
        try:
            data=request.data
            regions = data.get('regions')
            regions = [region['code'] for region in regions]
            regions = Region.objects.filter(code__in=regions).values_list('id', flat=True)
            data['regions'] = regions
            serializer = ZoneSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            zone = serializer.save()
            methods = data.get('methods')
            for method in methods:
                if Method.objects.filter(id=method['id']).exists():
                    pass
                else:
                    method['zone'] = zone.id
                    serializer = MethodSerializer(data=method)
                    serializer.is_valid(raise_exception=True)
                    method_instance = serializer.save()
                    if method['type'] == 'flate_rate':
                        shipping_classes = method.get('shipping_classes')
                        for shipping_class, cost in shipping_classes.items():
                            instance = ShippingMethod.objects.create(
                                shipping_class = Shipping.objects.get(id = shipping_class),
                                shipping_method = method_instance,
                            )
                            if not isinstance(cost, (int, float)) and cost[-1] == '*':
                                instance.cost_qty = True
                                instance.cost = cost[:-1]
                            else:
                                instance.cost_qty = False
                                instance.cost = cost
                            instance.save()
                
        except Exception as e:
                print(e)
        return Response(status=status.HTTP_201_CREATED)

class ZoneUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def update(self, request, *args, **kwargs):
        try:
            data=request.data
            regions = data.get('regions')
            regions = [region['code'] for region in regions]
            regions = Region.objects.filter(code__in=regions).values_list('id', flat=True)
            data['regions'] = regions
            instance = self.get_object()
            serializer = ZoneSerializer(instance = instance, data=data)
            serializer.is_valid(raise_exception=True)
            zone = serializer.save()
            methods = data.get('methods')
            for method in methods:
                if Method.objects.filter(id=method['id']).exists():
                    instance = Method.objects.get(id=method['id'])

                    if not isinstance(method['flate_rate_cost'], (int, float)) and method['flate_rate_cost'][-1] == '*':
                        method['flate_rate_qty'] = True
                        method['flate_rate_cost'] = method['flate_rate_cost'][:-1]
                    else:
                        method['flate_rate_qty'] = False
                        method['flate_rate_cost'] = method['flate_rate_cost']

                    if not isinstance(method['local_pickup_cost'], (int, float)) and method['local_pickup_cost'] and method['local_pickup_cost'][-1] == '*':
                        method['local_pickup_qty'] = True
                        method['local_pickup_cost'] = method['local_pickup_cost'][:-1]
                    else:
                        method['local_pickup_qty'] = False
                        method['local_pickup_cost'] = method['local_pickup_cost']
                    serializer = MethodSerializer(instance=instance, data=method)
                    serializer.is_valid(raise_exception=True)

                    method_instance = serializer.save()

                    if method['type'] == 'flat_rate':
                        shipping_classes = method.get('shipping_classes')
                        
                        shipping_classes_ids = []
                        for shipping_class, cost in shipping_classes.items():
                            if method_instance.classes.filter(shipping_class__id = shipping_class).exists():
                                instance = method_instance.classes.get(shipping_class__id = shipping_class)
                                if cost == '' or cost == None:
                                    instance.delete()
                                else:
                                    if not isinstance(cost, (int, float)) and cost[-1] == '*':
                                        instance.cost_qty = True
                                        instance.cost = cost[:-1]
                                    else:
                                        instance.cost_qty = False
                                        instance.cost = cost
                                    instance.save()
                            else:
                                instance = ShippingMethod.objects.create(
                                    shipping_class = Shipping.objects.get(id = shipping_class),
                                    shipping_method = method_instance,
                                )
                                if not isinstance(cost, (int, float)) and cost[-1] == '*':
                                    instance.cost_qty = True
                                    instance.cost = cost[:-1]
                                else:
                                    instance.cost_qty = False
                                    instance.cost = cost
                                instance.save()
                            shipping_classes_ids.append(instance.id)
                else:
                    method['zone'] = zone.id
                    if not isinstance(method['flate_rate_cost'], (int, float)) and method['flate_rate_cost'][-1] == '*':
                        method['flate_rate_qty'] = True
                        method['flate_rate_cost'] = method['flate_rate_cost'][:-1]
                    else:
                        method['flate_rate_qty'] = False
                        method['flate_rate_cost'] = method['flate_rate_cost']

                    if not isinstance(method['local_pickup_cost'], (int, float)) and method['local_pickup_cost'][-1] == '*':
                        method['local_pickup_qty'] = True
                        method['local_pickup_cost'] = method['local_pickup_cost'][:-1]
                    else:
                        method['local_pickup_qty'] = False
                        method['local_pickup_cost'] = method['local_pickup_cost']
                    print(method['local_pickup_qty'],method['local_pickup_cost'])
                    serializer = MethodSerializer(data=method)
                    serializer.is_valid(raise_exception=True)
                    method_instance = serializer.save()
                    if method['type'] == 'flate_rate':
                        shipping_classes = method.get('shipping_classes')
                        for shipping_class, cost in shipping_classes.items():
                            instance = ShippingMethod.objects.create(
                                shipping_class = Shipping.objects.get(id = shipping_class),
                                shipping_method = method_instance,
                            )
                            if not isinstance(cost, (int, float)) and cost[-1] == '*':
                                instance.cost_qty = True
                                instance.cost = cost[:-1]
                            else:
                                instance.cost_qty = False
                                instance.cost = cost

            
            Method.objects.filter(id__in=data.get('deletes')).delete()
        except Exception as e:
            print(e)
        return Response(status=status.HTTP_200_OK)
