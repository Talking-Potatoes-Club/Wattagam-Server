from django.db import models


class Account(models.Model):
    # 유저 정보 저장
    user_name = models.TextField(max_length=20, null=False)
    login_id = models.TextField(max_length=20, null=False)  # todo: email? or custom id?
    password = models.TextField(max_length=20, null=False)

    class Meta:
        db_table = "accounts"  # 이상한 이름으로 변경될 수 있어서 명시하는 것이 좋다고 함


class Follow(models.Model):
    # 팔로워 정보 저장
    from_user = models.ForeignKey(Account, related_name="follower", on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, related_name="following", on_delete=models.CASCADE)

    class Meta:
        db_table = "follows"
