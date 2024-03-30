
from django.urls import path, include
from . import views
urlpatterns = [
    # path("<str:title>/", views.CouponRetrieveView.as_view()),
    path("verify/", views.verify_coupons),
    path("<str:title>/", views.verify_new_coupon),
]