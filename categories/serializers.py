from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
