from django.urls import path

from ads import views

urlpatterns = [
    path("ad/", views.choose_method({
        "GET": views.AdListView.as_view(),
        "POST": views.AdCreateView.as_view(),
    }), name="ad-list"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad-detail-and-create"),
]
