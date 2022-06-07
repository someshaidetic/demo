from django import views
from django.urls import path
from .views import call, playAudio, interact, callback

urlpatterns = [
    path("calls", call),
    path("play", playAudio),
    path("interact", interact),
    path("recording/callback", callback),
]
