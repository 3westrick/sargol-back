
from django.urls import path, include
from . import views
urlpatterns = [
    # group
    path("groups/", views.WidgetGroupListView.as_view()),


    # options
    # path("", views.WidgetListView.as_view()),
    path("create/", views.WidgetCreateView.as_view()),
    path("<int:pk>/", views.WidgetRetriveView.as_view()),
    path("edit/<int:pk>/", views.WidgetUpdateView.as_view()),
    path("delete/<int:pk>/", views.WidgetDeleteView.as_view()),
]