
from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.ProductListView.as_view()),
    path("coupon/", views.ProductCouponListView.as_view()),
    path("create/", views.ProductCreateView.as_view()),
    path("variant/create/", views.VariantCreateView.as_view()),
    path("<int:pk>/", views.ProductRetriveView.as_view()),
    path("edit/<int:pk>/", views.ProductUpdateView.as_view()),
    path("variant/edit/<int:pk>/", views.VariantEditView.as_view()),
    path("delete/<int:pk>/", views.ProductDeleteView.as_view()),
    path("gallery/<int:pk>/", views.ProductGalleryDeleteView.as_view()),
]