from base.models import User
from rest_framework import generics
from base.serializers import UserSerializer, UserTestSerial
from base.mixins import CheckAuth
from rest_framework.response import Response
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer


class RetrieveUserProfile(CheckAuth, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial

    def get_object(self):
        return self.request.user
    
class UpdateUserProfile(CheckAuth, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTestSerial

    def get_object(self):
        return self.request.user