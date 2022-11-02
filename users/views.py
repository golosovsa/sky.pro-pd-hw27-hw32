from django.db.models import Prefetch
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from locations.models import Location
from users.models import User
from users.serializers import UserModelSerializer
from users.permissions import UserModeratorPermissions, UserAdminPermissions, UserOwnerPermissions

user_prefetch_query = User.objects.prefetch_related(
    Prefetch(
        "locations",
        queryset=Location.objects.only("id", "name")
    )
)


class UserCreateAPIView(CreateAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer
    permission_classes = []


class UserListApiView(ListAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, ]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, UserModeratorPermissions | UserAdminPermissions | UserOwnerPermissions]


class UserUpdateAPIView(UpdateAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, UserModeratorPermissions | UserAdminPermissions | UserOwnerPermissions]


class UserDestroyAPIView(DestroyAPIView):
    queryset = user_prefetch_query
    serializer_class = [IsAuthenticated, UserAdminPermissions]
