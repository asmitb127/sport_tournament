from django.contrib import admin
from django.urls import path, include 

from views import SportView

urlpatterns = [
    path('fetch/', SportView.as_view(), name='fetch')

]