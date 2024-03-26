from django.urls import path
from . import views
urlpatterns = [
    path("", views.PermissionsListView.as_view()),
]