from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from account.manage import CustomUserManager


class Account(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    # 유저 정보 저장
    user_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, max_length=255, null=False)  # todo: email? or custom id?
    #password = models.TextField(max_length=20, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Follow(models.Model):
    # 팔로워 정보 저장
    from_user = models.ForeignKey(Account, related_name="follower", on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, related_name="following", on_delete=models.CASCADE)

