from rest_framework.serializers import ModelSerializer

from locations.models import Location


class LocationModelSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
