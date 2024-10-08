
from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.ProductListView.as_view()),
    path("basket/", views.ProductBasketListView.as_view()),
    path("<str:slug>/", views.ProductRetriveView.as_view()),
]