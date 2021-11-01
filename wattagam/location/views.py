import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

from location.models import Picture
from location.models import MapLocation


@api_view(['POST'])
def newPictureView(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    picture = Picture.objects.create(author=user, picture=data['img_base64'])
    new_location = MapLocation.objects.filter(x_location=data['x_location'], y_location=data['y_location'])

    if new_location.exists():
        picture.location = new_location[0]
    else:
        new_location = MapLocation.objects.create(x_location=data['x_location'], y_location=data['y_location'],
                                                  location_name=data['location_name'])
        new_location.save()
        picture.location = new_location

    picture.save()

    return JsonResponse({'message': "게시글 업로드 완료", 'picture': picture.picture}, status=200)
