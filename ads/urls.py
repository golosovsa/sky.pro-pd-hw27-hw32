from django.urls import path
from django.conf.urls.static import static

from zavito import settings
from ads import views

urlpatterns = [
    path("ad/", views.AdListApiView.as_view(), name="ad-list-api"),
    path("ad/create/", views.AdCreateAPIView.as_view(), name="ad-create-api"),
    path("ad/<int:pk>/", views.AdRetrieveAPIView.as_view(), name="ad-detail-api"),
    path("ad/<int:pk>/update/", views.AdUpdateAPIView.as_view(), name="ad-update-api"),
    path("ad/<int:pk>/delete/", views.AdDestroyAPIView.as_view(), name="ad-delete-api"),
    path("ad/<int:pk>/upload_image/", views.AdUploadAPIView.as_view(), name="ad-upload-api"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
