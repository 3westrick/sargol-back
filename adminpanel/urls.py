from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("attributes/", include('adminpanel.attribute.urls')),
    path("values/", include('adminpanel.value.urls')),
    path("categories/", include('adminpanel.category.urls')),
    path("products/", include('adminpanel.product.urls')),
    path("coupons/", include('adminpanel.coupon.urls')),
    path("users/", include('adminpanel.user.urls')),
    path("permissions/", include('adminpanel.permissions.urls')),
    path("groups/", include('adminpanel.groups.urls')),
    path("orders/", include('adminpanel.order.urls')),
]
