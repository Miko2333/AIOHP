# frontend/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', index, name='index'),
	path('signup', signup_view, name='signup'),
	path('user', user, name='user'),
	path('course', course, name='course'),
]
