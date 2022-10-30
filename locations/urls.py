from rest_framework import routers

from locations import views


router = routers.SimpleRouter()
router.register("loc", views.LocationViewSet)

urlpatterns = router.urls
