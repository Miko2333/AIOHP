# frontend/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', index, name='index'),
	path('signup', signup_view, name='signup'),
	path('student_info', student_info, name='student_info'),
	path('teacher_info',teacher_info, name='teacher_info'),
	path('courses/', courses, name='courses'),
     path('course/create/', course_create_view, name='course-create'),
    path('course/<int:id>/', course_detail_view, name='course-detail'),
	path('course/<int:course_id>/teacher/<int:teacher_id>/', course_assignment_view, name='course_assignment'),
    path('course/<int:course_id>/teacher/<int:teacher_id>/create_assignment/', course_assignment_create_view, name='course_assignment_create'),
	path('course/<int:course_id>/student/<int:student_id>/', course_assignment_student_view, name='course_assignment_student'),
	path('course/<int:course_id>/homework/<int:homework_id>/student/<int:student_id>', homework_detail_student_view, name='homework_detail'),
	path('submit/',submit_homework, name='submit_homework'),
	path('submission/course/<int:course_id>/homework/<int:homework_id>/student/<int:student_id>/', submission_list, name='submission_list'),
	path('submission/<int:pk>/homework/<int:homework_id>/course/<int:course_id>/student/<int:student_id>/', submission_detail, name='submission_detail'),
	path('submission/course/<int:course_id>/homework/<int:homework_id>/', submission_list_teacher, name='submission_list_teacher'),
]
