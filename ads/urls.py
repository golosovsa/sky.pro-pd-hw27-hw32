from django.urls import path

from ads import views

urlpatterns = [
    path("", views.hello, name="hello"),
]
