from django.db import models


class Account(models.Model):
    # 유저 정보 저장
    user_name = models.TextField(max_length=20, null=False)
    login_id = models.TextField(max_length=20, null=False)  # todo: email? or custom id?
    password = models.TextField(max_length=20, null=False)


class Follow(models.Model):
    # 팔로워 정보 저장
    from_user = models.ForeignKey(Account, related_name="follower", on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, related_name="following", on_delete=models.CASCADE)