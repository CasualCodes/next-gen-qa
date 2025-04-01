from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("process_data", views.process_data, name="process_data"),
    path("cancel_scraping", views.cancel_scraping, name="cancel_scraping"),
    path("process_results", views.process_results, name="process_results"),
    path("cancel_generation", views.cancel_generation, name="cancel_generation"),
    path("results", views.results, name="results"),
    path("static_results", views.static_results, name="static_results"),
    path("download", views.download, name="download"),
    path("download_pdf", views.download_pdf, name="download_pdf"),
]