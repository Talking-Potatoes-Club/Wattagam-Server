from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_name = serializers.CharField()
    email = serializers.EmailField()
    bio = serializers.CharField()
    is_open = serializers.BooleanField()
    profile_img = serializers.ImageField()
