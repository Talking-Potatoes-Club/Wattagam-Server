import base64
import json
import uuid

from django.core.files.base import ContentFile
from django.db.models import Count
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

    picture = Picture.objects.create(author=user, picture=image, contents=data['contents'])

    cal_x = (data['x_location']*1000 - (data['x_location']*1000 % 1)) / 1000
    cal_y = (data['y_location']*1000 - (data['y_location']*1000 % 1)) / 1000

    new_location = MapLocation.objects.filter(x_location=cal_x, y_location=cal_y)
    if new_location.exists():
        picture.location = new_location[0]
    else:
        new_location = MapLocation.objects.create(x_location=cal_x, y_location=cal_y,
                                                  location_name=data['location_name'])
        new_location.save()
        picture.location = new_location

    picture.save()

    return JsonResponse({'message': "게시글 업로드 완료", 'post': PictureSerializer(picture).data}, status=200)


@api_view(['GET'])
def getPicture(request, location_id):

    location = MapLocation.objects.filter(id=location_id)
    if not location.exists():
        return JsonResponse({'message': "해당 위치에 등록된 사진이 없어용"}, status=200)

    posts = Picture.objects.filter(location=location[0])
    return JsonResponse({'message': "게시글 조회 완료", 'count': str(posts.count()),
                         'posts': PictureSerializer(posts, many=True).data}, status=200)


@api_view(['GET'])
def getLocationCount(request):
    cur_x = float(request.GET['x'])
    cur_y = float(request.GET['y'])

    posts = Picture.objects.filter(location__x_location__range=(cur_x - 0.01, cur_x + 0.01),
                                   location__y_location__range=(cur_y - 0.01, cur_y + 0.01))\
        .values('location', 'location__x_location', 'location__y_location', 'location__location_name')\
        .annotate(location_count=Count('location'))

    data = []
    for post in posts:
        data.append({'location_count': post['location_count'], 'location_id': post['location'],
                     'x_location': post['location__x_location'], 'y_location': post['location__y_location'],
                     'location_name': post['location__location_name']})

    return JsonResponse({'message': "조회 완료", 'mapLocation': data}, status=200)


""""@api_view(['GET'])
def getMyPictures(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()"""


@api_view(['DELETE'])
def deleteMyPicture(request, picture_id):
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    picture = Picture.objects.filter(id=picture_id)
    if not picture.exists():
        return JsonResponse({'message': '해당 사진이 존재하지 않습니다.'}, status=400)

    if picture[0].author.id == user.id:  # 본인 사진일 경우만 삭제 가능
        picture[0].delete()
        return JsonResponse({'message': '사진 삭제 완료.'}, status=200)
    else:
        return JsonResponse({'message': '사진을 삭제할 권한이 없습니다.'}, status=403)
