from django.urls import path
from location.views import *
import location

urlpatterns = [
    path('newPicture', location.views.newPictureView, name='newPictureView'),
    path('getPictures/<int:location_id>', location.views.getPicture, name='getPicture'),
    path('getLocationCount', location.views.getLocationCount, name='getLocationCount'),
    #path('myPicture', location.views.getMyPictures, name='getMyPictures'),
    path('myPicture/<int:picture_id>', location.views.deleteMyPicture, name='deleteMyPicture'),
]
