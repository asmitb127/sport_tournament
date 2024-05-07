from django.contrib import admin
from django.urls import path, include 

from sport.views import SportView, SportList

urlpatterns = [
    path('fetch/', SportView.as_view(), name='fetch'),
    path('sports/', SportList.as_view(), name='sportlist')

]