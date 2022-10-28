from django.urls import path

from categories import views


urlpatterns = [
    path("cat/", views.CategoryListView.as_view(), name="category-list"),
    path("cat/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("cat/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("cat/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("cat/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),
]
