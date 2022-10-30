from django.urls import path

from users import views


urlpatterns = [
    path("user/", views.UserListApiView.as_view(), name="user-list"),
    path("user/create/", views.UserCreateAPIView.as_view(), name="user-create"),
    path("user/<int:pk>/", views.UserRetrieveAPIView.as_view(), name="user-detail"),
    path("user/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user-update"),
    path("user/<int:pk>/delete/", views.UserDestroyAPIView.as_view(), name="user-delete"),
]
