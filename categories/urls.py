# from django.urls import path
from rest_framework.routers import DefaultRouter

from categories import views


router = DefaultRouter()
router.register("cat", views.CategoryViewSet, basename="category")

urlpatterns = router.urls
