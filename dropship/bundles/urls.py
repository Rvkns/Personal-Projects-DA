"""URL routing for bundles app."""

from django.urls import path

from . import views

app_name = "bundles"

urlpatterns = [
    path("", views.BundleListView.as_view(), name="bundle_list"),
    path("<slug:slug>/", views.BundleDetailView.as_view(), name="bundle_detail"),
]
