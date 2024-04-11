
from django.urls import path, include
from . import views
urlpatterns = [

    path("", views.OrderListView.as_view()),

    path("purchase/", views.purchase),
    path("items/", views.ItemListView.as_view()),
    path("items/create/", views.ItemCreateView.as_view()),
    path("items/edit/<int:pk>/", views.ItemEditView.as_view()),
    path("items/delete/<int:pk>/", views.ItemDeleteView.as_view()),
    # path("", views.CategoryListView.as_view()),
    # path("create/", views.CategoryCreateView.as_view()),
    # path("<int:pk>/", views.CategoryRetriveView.as_view()),
    # path("edit/<int:pk>/", views.CategoryUpdateView.as_view()),
    # path("delete/<int:pk>/", views.CategoryDeleteView.as_view()),
]