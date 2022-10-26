from django.urls import path

from ads import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("cat/", views.choose_method({
        "GET": views.CategoryListView.as_view(),
        "POST": views.CategoryCreateView.as_view(),
    }), name="category-list-and-create"),
    path("cat/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("ad/", views.choose_method({
        "GET": views.AdListView.as_view(),
        "POST": views.AdCreateView.as_view(),
    }), name="ad-list"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad-detail-and-create"),
]
