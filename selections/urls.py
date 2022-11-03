from django.urls import path, URLPattern

from selections.views import \
    SelectionListView, \
    SelectionDetailDeleteView, \
    SelectionCreateView, \
    SelectionUpdateView


urlpatterns = [
    path("selection/", SelectionListView.as_view(), name="selection-list"),
    path("selection/create/", SelectionCreateView.as_view(), name="selection-create"),
    path("selection/<int:pk>/", SelectionDetailDeleteView.as_view(), name="selection-detail"),
    path("selection/<int:pk>/update/", SelectionUpdateView.as_view(), name="selection-update"),
]
