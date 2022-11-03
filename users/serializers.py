from rest_framework.serializers import ModelSerializer, SlugRelatedField, CharField

from locations.models import Location
from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

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

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(user.password)
        user.save()
        return user
