# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
	path('check_login_status/', check_login_status, name='check_login_status'),
    path('courses/', CourseList.as_view()),
    path('courses/<int:pk>', CourseDetail.as_view()),
    path('courses/<int:pk>/add_student', AddStudent.as_view()),
    path('courses/<int:pk>/remove_student', RemoveStudent.as_view()),
    path('students', StudentList.as_view()),
    path('students/<int:pk>', StudentDetail.as_view()),
    path('teachers', TeacherList.as_view()),
    path('teachers/<int:pk>', TeacherDetail.as_view()),
	
	
    path('homeworks', HomeworkList.as_view(), name='HomeworkList'),
    path('homeworks/<int:pk>', HomeworkDetail.as_view(), name='HomeworkDetail'),
    path('homeworks/<int:pk>/get_all_submission', GetAllSubmission.as_view(), name='GetAllSubmission'),
    path('homeworks/<int:pk>/get_submission/', GetSubmission.as_view(), name='GetSubmission'),

    path('submissions', SubmissionList.as_view(), name='SubmissionList'),
    path('submissions/<int:pk>', SubmissionDetail.as_view(), name='SubmissionDetail'),

    path('file', FileList.as_view(), name='FileList'), # only use for debug
    path('upload', FileUpload.as_view(), name='FileUpload'),
    path('download/<int:pk>', FileDownload.as_view(), name='FileDownload'),	


]
