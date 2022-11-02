from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad
from ads.permissions import AdOwnerPermissions
from ads.serializers import AdModelSerializerForSafeMethods, AdModelSerializerForWriteMethods, \
    AdModelUploadImageSerializer
from users.permissions import UserModeratorAndAdminCanWriteOrReadOnly


class AdListApiView(ListAPIView):
    queryset = Ad.objects.select_related("author").order_by("-price")
    serializer_class = AdModelSerializerForSafeMethods
    permission_classes = [IsAuthenticated, ]

    url_query_cat = "cat"
    url_query_text = "text"
    url_query_location = "location"
    url_query_price_from = "price_from"
    url_query_price_to = "price_to"

    # lookup_url_kwarg = [
    #     url_query_cat,
    #     url_query_text,
    #     url_query_location,
    #     url_query_price_from,
    #     url_query_price_to,
    # ]

    def get_queryset(self):
        queries = self.request.GET
        queryset = super().get_queryset()
        if query := queries.get(self.url_query_cat):
            queryset = queryset.filter(category_id=query)
        if query := queries.get(self.url_query_text):
            queryset = queryset.filter(name__icontains=query)
        if query := queries.get(self.url_query_location):
            queryset = queryset.filter(author__locations__name__icontains=query)
        if all(query := (queries.get(self.url_query_price_from), queries.get(self.url_query_price_to))):
            queryset = queryset.filter(Q(price__gte=query[0]) & Q(price__lte=query[1]))

        print(self.kwargs)

        return queryset


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.select_related("author")
    serializer_class = AdModelSerializerForSafeMethods
    permission_classes = [IsAuthenticated, ]


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdModelSerializerForWriteMethods
    permission_classes = [IsAuthenticated, ]


class AdUpdateAPIView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdModelSerializerForWriteMethods
    permission_classes = [IsAuthenticated, AdOwnerPermissions | UserModeratorAndAdminCanWriteOrReadOnly]


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdModelSerializerForWriteMethods
    permission_classes = [IsAuthenticated, AdOwnerPermissions | UserModeratorAndAdminCanWriteOrReadOnly]


class AdUploadAPIView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdModelUploadImageSerializer
    permission_classes = [IsAuthenticated, AdOwnerPermissions | UserModeratorAndAdminCanWriteOrReadOnly]
