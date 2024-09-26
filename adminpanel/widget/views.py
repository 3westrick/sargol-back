from adminpanel.widget.serial import WidgetGroupSerial, WidgetSerial,WidgetCreateSerial, WidgetUpdateSerial
from rest_framework import generics
from base.mixins import CheckPermission
from base.pagination import CustomLimitOffsetPagtination
from base.filters import CustomSearch, CustomFilter
from widget.models import Widgetgroup, Widget

class WidgetGroupListView(CheckPermission, CustomSearch,generics.ListAPIView):
    queryset = Widgetgroup.objects.all()
    serializer_class = WidgetGroupSerial



class WidgetListView(CheckPermission, CustomFilter,generics.ListAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerial
    filterset_fields = {
        "group__type": ["exact"],
    }
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class WidgetCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetCreateSerial
    
class WidgetUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetUpdateSerial
    lookup_field = 'pk'

    
class WidgetRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetCreateSerial
    lookup_field = 'pk'


class WidgetDeleteView(CheckPermission, generics.DestroyAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetCreateSerial
    lookup_field = 'pk'

