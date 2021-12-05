from rest_framework import serializers

from location.models import MapLocation
from location.models import Picture

from account.serializers import AccountSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLocation
        fields = ('id', 'x_location', 'y_location', 'location_name')


class PictureSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    author = AccountSerializer()

    class Meta:
        model = Picture
        fields = ('id', 'location', 'created_at', 'author', 'picture', 'contents')

