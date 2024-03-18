from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view())
]
