from django.urls import path
from location.views import *
import location

urlpatterns = [
    path('newPicture', location.views.newPictureView, name='newPictureView'),
]
