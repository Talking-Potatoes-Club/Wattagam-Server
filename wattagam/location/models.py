from django.db import models
from account.models import Account  # ?? 그지같은 파이썬. 오히려 경로 맞춰준다고 wattagam 넣으니 migrate못함. model 가져오는 부분이 다른듯


class Picture(models.Model):
    # 유저가 찍은 사진과 위치 정보 저장
    x_location = models.FloatField()
    y_location = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    picture = models.TextField()

    class Meta:
        db_table = "pictures"


class MapLocation(models.Model):
    # 구글 api에서 가져온 위치 정보 따로 저장. 맵 api 정보 보고 추가 or 삭제
    x_location = models.FloatField()
    y_location = models.FloatField()
    location_name = models.TextField()

    class Meta:
        db_table = "mapLocations"

