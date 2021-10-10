import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from account.models import Account


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        Account(
            login_id=data['login_id'],
            password=data['password'],
            user_name=data['user_name']
        ).save()

        return JsonResponse({'message': '회원가입 완료'}, status=200)


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Account.objects.filter(login_id=data['login_id']).exists():
            user = Account.objects.get(login_id=data['login_id'])
            if user.password == data['password']:
                return JsonResponse({'message': f'{user.login_id}님 로그인 성공!'}, status=200)
            else:
                return JsonResponse({'message': '비밀번호가 틀렸어요'}, status=401)

        return JsonResponse({'message': '등록되지 않은 아이디 입니다.'}, status=401)
