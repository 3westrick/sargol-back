from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("attributes/", include('adminpanel.attribute.urls')),
    path("values/", include('adminpanel.value.urls')),
    path("categories/", include('adminpanel.category.urls')),
    path("products/", include('adminpanel.product.urls')),
]
