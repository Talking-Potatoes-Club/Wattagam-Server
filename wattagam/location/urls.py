from django.urls import path
from location.views import *
import location

urlpatterns = [
    path('newPicture', location.views.newPictureView, name='newPictureView'),
    path('getPicture/<int:location_id>', location.views.getPicture, name='getPicture'),
    path('getLocationCount', location.views.getLocationCount, name='getLocationCount'),
]
