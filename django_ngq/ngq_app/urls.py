from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("loading", views.loading, name="loading"),
    path("results", views.results, name="results"),
    path("process_data", views.process_data, name="process_data"),
    path("download", views.download, name="download"),
    path("download_pdf", views.download_pdf, name="download_pdf"),
    path("loading_results", views.loading_results, name="loading_results")
]