from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


class CustomUserSerializer(UserCreateSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ("first_name", "last_name")
