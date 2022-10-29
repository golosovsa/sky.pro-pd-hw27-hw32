from django.urls import path

from users import views


urlpatterns = [
    path("user/", views.UserListView.as_view(), name="user-list"),
    path("user/create/", views.UserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("user/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
