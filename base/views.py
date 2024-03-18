from django.shortcuts import render
from base.models import User
from rest_framework import permissions, generics
from base.serializers import UserSerializer
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer