from rest_framework.serializers import ModelSerializer, SlugRelatedField, CharField
from django.contrib.auth.hashers import make_password

from locations.models import Location
from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    locations = SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="name",
        queryset=Location.objects.only("id", "name"),
    )

    password = CharField(
        max_length=20,
        write_only=True,
        required=True,
    )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
