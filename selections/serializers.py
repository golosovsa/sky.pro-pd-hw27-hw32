from rest_framework.serializers import ModelSerializer, SlugRelatedField, HyperlinkedRelatedField, RelatedField, ManyRelatedField

from ads.serializers import AdModelDefaultSerializer
from selections.models import Selection


class SelectionDefaultSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionListSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"

    items = AdModelDefaultSerializer(many=True)
