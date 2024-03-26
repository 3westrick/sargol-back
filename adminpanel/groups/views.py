from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from base.mixins import CheckPermission
from base.pagination import ModelPaginateAndFilterSecond
from rest_framework import generics
from adminpanel.groups.serial import GroupSerial


class GroupsListView(CheckPermission, generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerial


class GroupsListAPI(CheckPermission, ModelPaginateAndFilterSecond, generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerial
    search_fields = ['id', 'name', 'permissions__name']
    ordering_fields = ['id','name']


class GroupsCreateView(CheckPermission, generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerial

class GroupsRetrieveView(CheckPermission, generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerial
    lookup_field="pk"

class GroupsUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerial
    lookup_field="pk"