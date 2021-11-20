import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from account.models import Account
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.serializers import AccountSerializer
from location.models import Picture
from location.serializers import PictureSerializer


@permission_classes((AllowAny,))
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        user = Account.objects.create_user(
            email=data['email'],
            password=data['password'],
            user_name=data['user_name'],
            bio=data['bio']
        )

        if user:
            return JsonResponse({'message': '회원가입 완료'}, status=200)
        else:
            return JsonResponse({'message': '회원가입 실패'}, status=400)


@permission_classes((AllowAny,))
class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if data['email'] is None or data['password'] is None:
            return JsonResponse({'message': '아이디와 비밀번호를 입력해 주십시오'}, status=400)

        account = authenticate(email=data['email'], password=data['password'])

        if not account:
            return JsonResponse({'message': '등록되지 않은 아이디 입니다.'}, status=401)

        token, _ = Token.objects.get_or_create(user=account)

        return JsonResponse({'message': f'{account.user_name}님 로그인 성공!', 'token': token.key,
                             'userInfo': AccountSerializer(account).data}, status=200)


@permission_classes((AllowAny,))
class TempPasswordView(View):
    def post(self, request):
        data = json.loads(request.body)

        if data['email'] is None:
            return JsonResponse({'message': '임시 비밀번호를 발급할 이메일을 입력해 주십시오'}, status=400)

        password = User.objects.make_random_password()
        user = Account.objects.filter(email=data['email'])[0]

        user.set_password(password)
        user.save()

        return JsonResponse({'message': '임시 비밀번호가 발급되었습니다.', 'temp_password': password}, status=200)


@api_view(['PATCH'])  # 하 ㅋㅋ 클래스로 만들면 auth 안타고 그냥 def로 해야 타네, 이유를 모르겠다
def changePasswordView(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    if check_password(data['origin_password'], user.password):
        user.set_password(data['new_password'])
        user.save()

        return JsonResponse({'message': '비밀번호 변경이 완료되었습니다.'}, status=200)

    else:
        return JsonResponse({'message': '기존 비밀번호가 틀렸습니다.'}, status=400)


@api_view(['PATCH'])
def changeNicknameView(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    if Account.objects.filter(user_name=data['new_name']).exists():
        return JsonResponse({'message': '같은 닉네임이 존재합니다.'}, status=500)

    else:
        user.user_name = data['new_name']
        user.save()

        return JsonResponse({'message': '닉네임 변경이 완료되었습니다.'}, status=200)


@api_view(['PATCH'])
def changeUserInfo(request):
    data = json.loads(request.body)
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    user.bio = data['bio']

    if data['is_open']:
        user.is_open = True
    else:
        user.is_open = False

    user.save()
    return JsonResponse({'message': '유저 정보 변경 완료되었습니다.', 'userInfo': AccountSerializer(user).data}, status=200)


@api_view(['GET'])
def getUserInfo(request, user_id):
    user = Account.objects.filter(id=user_id)

    if user.exists():  # is_open인 상태면 해당 유저 사진까지 보냄. todo: 친구 기능 추가
        if user[0].is_open or request.user is user[0]:
            pictures = Picture.objects.filter(author=user[0])  # todo: pagination 추가
            return JsonResponse({'message': '유저 정보 열람 완료.', 'userInfo': AccountSerializer(user[0]).data,
                                 'pictures': PictureSerializer(pictures, many=True).data})
        else:
            return JsonResponse({'message': '유저 정보 열람 완료.', 'userInfo': AccountSerializer(user[0]).data}, status=200)

    else:
        return JsonResponse({'message': '해당 유저가 없습니다.'}, status=400)


@api_view(['DELETE'])
def deleteUser(request):
    user = request.user

    if request.user.is_anonymous:
        raise AuthenticationFailed()

    Picture.objects.filter(author=user).delete()  # 저장된 해당 유저 사진 삭제
    user.delete()
    logout(request)

    return JsonResponse({'message': '회원 탈퇴되었습니다.'}, status=200)

