from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ShippingListView.as_view()),
    path("all/", views.ShippingAllListView.as_view()),
    path("<int:pk>/", views.ShippingRetrieveView.as_view()),
    path("create/", views.ShippingCreateView.as_view()),
    path("edit/<int:pk>/", views.ShippingUpdateView.as_view()),
    path("delete/<int:pk>/", views.ShippingDeleteView.as_view()),


    path("zones/", views.ZoneListView().as_view()),
    path("zones/create/", views.ZoneCreateView().as_view()),
    path("zones/<int:pk>/", views.ZoneRetrieveView().as_view()),
    path("zones/edit/<int:pk>/", views.ZoneUpdateView().as_view()),
]