from rest_framework.response import Response
from rest_framework.decorators import api_view
from order.serial import OrderSerial, ItemSerial, ItemSerialCreate, ItemListSerial
from rest_framework.exceptions import NotFound

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from base.mixins import CheckAuth


from widget.models import Widgetgroup, Widget
from rest_framework import generics
from widget.serial import WidgetGroupSerial
from rest_framework.response import Response


# Create your views here.
class WidgetGroupListView(generics.RetrieveAPIView):
    queryset = Widgetgroup.objects.all()
    serializer_class = WidgetGroupSerial
    lookup_field='slug'

# @api_view(['GET'])
# def single_widget_group(request, slug):
#     wg = Widgetgroup.objects.get(slug=slug)
#     widgets = WidgetGroupSerial(wg)
#     return Response(widgets.data)