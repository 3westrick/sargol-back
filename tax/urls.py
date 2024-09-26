from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaxList().as_view())
]