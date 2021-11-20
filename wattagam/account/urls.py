from django.urls import path
from account.views import *
import account

urlpatterns = [
    path('signUp', SignUpView.as_view()),
    path('logIn', LogInView.as_view()),
    path('tempPassword', TempPasswordView.as_view()),
    path('changePassword', account.views.changePasswordView, name='changePasswordView'),
    path('changeNickname', account.views.changeNicknameView, name='changeNicknameView'),
    path('changeUserInfo', account.views.changeUserInfo, name='changeUserInfo'),
    path('getUserInfo/<int:user_id>', account.views.getUserInfo, name='getUserInfo'),
    path('deleteUser', account.views.deleteUser, name='deleteUser'),
]
