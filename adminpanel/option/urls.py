from django.urls import path, include
from . import views

urlpatterns = [
    path('shippings/', views.ShippingOptionsList().as_view()),
    path('shippings/edit/', views.ShippingOptionsUpdate().as_view()),

    path('taxes/', views.TaxOptionsList().as_view()),
    path('taxes/edit/', views.TaxOptionsUpdate().as_view()),

    path('general/', views.GeneralOptionsList().as_view()),
    path('general/edit/', views.GeneralOptionsUpdate().as_view()),
]