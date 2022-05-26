from django import views
from django.urls import path
from .views import Call,PlayAudio

urlpatterns = [
    path('calls',Call),
    path('play',PlayAudio),
]