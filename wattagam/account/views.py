import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from account.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@permission_classes((AllowAny,))
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        """Account(
            email=data['email'],
            password=data['password'],
            user_name=data['user_name']
        ).save()"""
        user = Account.objects.create_user(
            email=data['email'],
            password=data['password'],
            user_name=data['user_name']
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

        return JsonResponse({'message': f'{account.user_name}님 로그인 성공!', 'token': token.key}, status=200)

        """if Account.objects.filter(login_id=data['login_id']).exists():
            user = Account.objects.get(login_id=data['login_id'])
            if user.password == data['password']:
                return JsonResponse({'message': f'{user.login_id}님 로그인 성공!'}, status=200)
            else:
                return JsonResponse({'message': '비밀번호가 틀렸어요'}, status=401)

        return JsonResponse({'message': '등록되지 않은 아이디 입니다.'}, status=401)"""
