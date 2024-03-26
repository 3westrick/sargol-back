from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import  OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class MyLimitOffsetPagtination(LimitOffsetPagination):
    default_limit = 10

class ModelPaginateAndFilter():
    pagination_class = MyLimitOffsetPagtination
    filter_backends = [SearchFilter, OrderingFilter, ]

class ModelPaginateAndFilterSecond():
    pagination_class = MyLimitOffsetPagtination
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter, ]