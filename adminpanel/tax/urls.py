from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaxListView.as_view()),
    path("all/", views.TaxAllListView.as_view()),
    path("<int:pk>/", views.TaxRetrieveView.as_view()),
    path("create/", views.TaxCreateView.as_view()),
    path("edit/<int:pk>/", views.TaxUpdateView.as_view()),
    path("delete/<int:pk>/", views.TaxDeleteView.as_view()),


    path("rates/", views.RateListView.as_view()),
    path("rates/create/", views.RateCreateView.as_view()),
    path("rates/edit/<int:pk>/", views.RateUpdateView.as_view()),
]