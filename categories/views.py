from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from categories.models import Category
from users.permissions import UserModeratorAndAdminCanWriteOrReadOnly
from categories.serializers import CategoryModelSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated, UserModeratorAndAdminCanWriteOrReadOnly, ]

