
from django.urls import path
from . import views
urlpatterns = [
    path("", views.UserListView.as_view()),
    path("create/", views.UserCreateView.as_view()),
    path("<int:pk>/", views.UserRetriveView.as_view()),
    path("edit/<int:pk>/", views.UserUpdateView.as_view()),
]