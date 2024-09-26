from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view()),
    path("profile/", views.RetrieveUserProfile.as_view()),
    path("profile/edit/", views.UpdateUserProfile.as_view()),

]
