from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from base.mixins import CheckPermission
from base.pagination import ModelPaginateAndFilterSecond
from rest_framework import generics
from adminpanel.permissions.serial import PermissionSerial


class PermissionsListView(CheckPermission, generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerial