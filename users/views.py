from django.db.models import Prefetch
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from locations.models import Location
from users.models import User
from users.serializers import UserModelSerializer

user_prefetch_query = User.objects.prefetch_related(
    Prefetch(
        "locations",
        queryset=Location.objects.only("id", "name")
    )
)


class UserCreateAPIView(CreateAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer


class UserListApiView(ListAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer


class UserDestroyAPIView(DestroyAPIView):
    queryset = user_prefetch_query
    serializer_class = UserModelSerializer
