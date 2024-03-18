
from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.CategoryListView.as_view()),
    path("product/", views.CategoryProductListView.as_view()),
    path("create/", views.CategoryCreateView.as_view()),
    path("<int:pk>/", views.CategoryRetriveView.as_view()),
    path("edit/<int:pk>/", views.CategoryUpdateView.as_view()),
    path("delete/<int:pk>/", views.CategoryDeleteView.as_view()),
]