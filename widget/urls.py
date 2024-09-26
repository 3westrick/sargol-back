
from django.urls import path
from . import views
urlpatterns = [
    # group
    path("groups/<str:slug>/", views.WidgetGroupListView.as_view()),
    # path("groups/<str:slug>/", views.single_widget_group),


    # options
    # path("", views.WidgetListView.as_view()),
    # path("create/", views.WidgetCreateView.as_view()),
    # path("<str:title>/", views.WidgetRetriveView.as_view()),
    # path("edit/<int:pk>/", views.WidgetUpdateView.as_view()),
    # path("delete/<int:pk>/", views.WidgetDeleteView.as_view()),
]