# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('courses', CourseList.as_view()),
    path('courses/<int:pk>', CourseDetail.as_view()),
    path('courses/<int:pk>/add_student', AddStudent.as_view()),
    path('courses/<int:pk>/remove_student', RemoveStudent.as_view()),
    path('students', StudentList.as_view()),
    path('students/<int:pk>', StudentDetail.as_view()),
    path('teachers', TeacherList.as_view()),
    path('teachers/<int:pk>', TeacherDetail.as_view()),
]
