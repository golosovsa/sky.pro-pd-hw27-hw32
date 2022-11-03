from rest_framework.serializers import \
    ModelSerializer, \
    SlugRelatedField, \
    PrimaryKeyRelatedField, \
    HyperlinkedModelSerializer

from ads.models import Ad


class AdModelDefaultSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdModelSerializerForSafeMethods(ModelSerializer):
    author = SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="first_name",
    )

    author_id = PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    category_id = PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Ad
        exclude = ["category", ]


class AdModelSerializerForWriteMethods(ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "description", "is_published", "category", ]


class AdModelUploadImageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Ad
        fields = ["image", ]
