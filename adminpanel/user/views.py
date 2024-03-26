from base.models import User
from adminpanel.user.serial import UserSerial, UserPermission,UserTestSerial
from rest_framework import generics
from base.mixins import CheckPermission
from base.pagination import ModelPaginateAndFilterSecond
import django_filters
# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact'],
            'email': ['exact'],
        }

class UserListView(CheckPermission, ModelPaginateAndFilterSecond, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial
    # search_fields = ['id','title', 'slug', 'description', 'short_description', 'sku', 'mpn', ]
    search_fields = ['id', 'username', 'email']
    ordering_fields = ['id','username', 'email']
    # filterset_class = UserFilter

class UserCreateView(CheckPermission, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial

        

class UserRetriveView(CheckPermission, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial
    lookup_field = 'pk'

class UserUpdateView(CheckPermission, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial
    lookup_field = 'pk'

@api_view(['GET'])
def user_persmissions(request, pk):
    user = User.objects.get(pk=pk)
    print(dir(user))
    permissions = Permission.objects.all()

    # for i in user.groups.all():
    #     print(i.name)
    # user.groups.add(group_obj)
    print()
    # for i in user.user_permissions.all():
    #     print(i.codename)
    # user.user_permissions.add(permissoin_obj)
    print()


    # get_all_permissions
    # get_group_permissions
    # get_user_permissions
    # groups
    # user_permissions
    return Response(status=200)