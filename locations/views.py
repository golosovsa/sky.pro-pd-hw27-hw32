from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from locations.models import Location
from locations.serializers import LocationModelSerializer
from users.permissions import UserModeratorAndAdminCanWriteOrReadOnly, UserOwnerPermissions


class LocationViewSet(ViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = [IsAuthenticated, UserModeratorAndAdminCanWriteOrReadOnly | UserOwnerPermissions, ]

    def list(self, request):
        queryset = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, self.request, view=self)
        if page:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        location = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(location)
        return Response(serializer.data)

    def update(self, request, pk=None, partial=False):
        location = get_object_or_404(self.queryset, pk=pk,)
        serializer = self.serializer_class(location, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk, partial=True)

    def destroy(self, request, pk=None):
        location = get_object_or_404(self.queryset, pk=pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
