from django.urls import path

from locations import views


urlpatterns = [
    path("loc/", views.LocationListView.as_view(), name="location-list"),
    path("loc/create/", views.LocationCreateView.as_view(), name="location-create"),
    path("loc/<int:pk>/", views.LocationDetailView.as_view(), name="location-detail"),
    path("loc/<int:pk>/update/", views.LocationUpdateView.as_view(), name="location-update"),
    path("loc/<int:pk>/delete/", views.LocationDeleteView.as_view(), name="location-delete"),
]
