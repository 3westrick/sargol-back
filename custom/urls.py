from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.CustomListView.as_view()),
    path("create/", views.CustomCreateView.as_view()),
    path("<int:pk>/", views.CustomRetriveView.as_view()),
    path("edit/<int:pk>/", views.CustomUpdateView.as_view()),
    path("delete/<int:pk>/", views.CustomDeleteView.as_view()),
]