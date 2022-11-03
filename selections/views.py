from rest_framework.generics import mixins, GenericAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Prefetch

from ads.models import Ad
from selections.models import Selection
from selections.permissions import IsSelectionOwner
from selections.serializers import SelectionDefaultSerializer, SelectionListSerializer, SelectionDetailSerializer
from users.permissions import UserModeratorAndAdminCanWriteOrReadOnly


class SelectionListView(mixins.ListModelMixin, GenericAPIView):
    queryset = Selection.objects.prefetch_related(
            Prefetch(
                "items",
                queryset=Ad.objects.only("name")
            ),
        ).all()
    serializer_class = SelectionListSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SelectionDetailDeleteView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Selection.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = SelectionDetailSerializer
        self.permission_classes = [AllowAny, ]
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.serializer_class = SelectionDefaultSerializer
        self.permission_classes = [IsAuthenticated, IsSelectionOwner | UserModeratorAndAdminCanWriteOrReadOnly, ]
        return self.destroy(request, *args, **kwargs)


class SelectionCreateView(mixins.CreateModelMixin, GenericAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDefaultSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SelectionUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDefaultSerializer
    permission_classes = [IsAuthenticated, IsSelectionOwner | UserModeratorAndAdminCanWriteOrReadOnly, ]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
