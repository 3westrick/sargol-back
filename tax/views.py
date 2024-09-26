from django.shortcuts import render
from rest_framework.decorators import api_view
from tax.models import Tax
from .serial import TaxSerial
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.
class TaxList(generics.ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerial