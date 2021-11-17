from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from location.models import MapLocation
from location.models import Picture

from account.serializers import AccountSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLocation
        fields = ('x_location', 'y_location', 'location_name')


class PictureSerializer(serializers.ModelSerializer):
    # picture = Base64ImageField()  # From DRF Extra Fields
    location = LocationSerializer(read_only=True)
    author = AccountSerializer()

    class Meta:
        model = Picture
        fields = ('location', 'created_at', 'author', 'picture')

