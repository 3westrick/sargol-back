from django.urls import path
from . import views

urlpatterns = [
    path('shippings/', views.ShippingOptionsList().as_view()),
    path('taxes/', views.TaxOptionsList().as_view()),
    path('generals/', views.GeneralOptionsList().as_view()),
]