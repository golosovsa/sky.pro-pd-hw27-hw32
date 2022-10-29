from django.urls import path
from django.conf.urls.static import static

from zavito import settings
from ads import views

urlpatterns = [
    path("ad/", views.AdListView.as_view(), name="ad-list"),
    path("ad/create/", views.AdCreateView.as_view(), name="ad-create"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(), name="ad-update"),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad-delete"),
    path("ad/<int:pk>/upload_image/", views.AdUploadView.as_view(), name="ad-upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
