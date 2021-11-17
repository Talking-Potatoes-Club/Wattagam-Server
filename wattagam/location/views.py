import base64
import json
import uuid

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

from location.models import Picture
from location.models import MapLocation

from location.serializers import PictureSerializer


@api_view(['POST'])
def newPictureView(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    image_name = str(uuid.uuid4())
    image_b64 = data['picture']  # This is your base64 string image
    image = ContentFile(base64.b64decode(image_b64), name=image_name+".png")

    picture = Picture.objects.create(author=user, picture=image)

    new_location = MapLocation.objects.filter(x_location=data['x_location'], y_location=data['y_location'])
    if new_location.exists():
        picture.location = new_location[0]
    else:
        new_location = MapLocation.objects.create(x_location=data['x_location'], y_location=data['y_location'],
                                                  location_name=data['location_name'])
        new_location.save()
        picture.location = new_location

    picture.save()

    return JsonResponse({'message': "게시글 업로드 완료", 'post': PictureSerializer(picture).data}, status=200)


@api_view(['GET'])
def getPicture(request, location_id):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    location = MapLocation.objects.filter(id=location_id)
    if not location.exists():
        return JsonResponse({'message': "해당 위치에 등록된 사진이 없어용"}, status=200)

    posts = Picture.objects.filter(location=location[0])
    return JsonResponse({'message': "게시글 조회 완료", 'count': str(posts.count()),
                         'posts': PictureSerializer(posts, many=True).data}, status=200)


@api_view(['GET'])
def getLocationCount(request):
    return JsonResponse()
