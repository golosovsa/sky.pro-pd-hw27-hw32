from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS

from selection.models import Selection


class SelectionModelViewSet(GenericAPIView):
    queryset = Selection.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            queryset = queryset.prefetch_related(
                "items",
                Prefetch()
            )
        return queryset
