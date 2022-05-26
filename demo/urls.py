from django import views
from django.urls import path
from .views import Call

urlpatterns = [
    path('calls',Call),
]