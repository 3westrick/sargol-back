from django.urls import path
from . import views
urlpatterns = [
    path("", views.GroupsListView.as_view()),
    path("list/", views.GroupsListAPI.as_view()),
    path("<int:pk>/", views.GroupsRetrieveView.as_view()),
    path("create/", views.GroupsCreateView.as_view()),
    path("edit/<int:pk>/", views.GroupsUpdateView.as_view()),
]