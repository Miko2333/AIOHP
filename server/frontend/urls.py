# frontend/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', index, name='index'),
	path('signup', signup_view, name='signup'),
	path('student_info', student_info, name='student_info'),
	path('teacher_info',teacher_info, name='teacher_info'),
	path('course', course, name='course'),
    path('course/create/', course_create_view, name='course-create'),
    path('course/<int:id>/', course_detail_view, name='course-detail'),
]
