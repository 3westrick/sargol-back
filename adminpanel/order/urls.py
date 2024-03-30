from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.OrderListView.as_view()),
    path("<int:pk>/", views.OrderRetrieveView.as_view()),
    # path("create/", views.CouponCreateView.as_view()),
    path("edit/<int:pk>/", views.OrderUpdateView.as_view()),
    # path("delete/<int:pk>/", views.CouponDeleteView.as_view()),
    # path("", ),
    # path("", ),
    # path("", ),
]