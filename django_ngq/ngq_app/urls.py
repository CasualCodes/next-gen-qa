from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("loading", views.loading, name="loading"),
    path("results", views.results, name="results"),
]