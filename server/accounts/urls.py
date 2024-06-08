# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('register', Register.as_view(), name='Register'),
    path('login', Login.as_view(), name='Login'),

    path('courses', CourseList.as_view(), name='CourseList'),
    path('courses/<int:pk>', CourseDetail.as_view(), name='CourseDetail'),
    path('courses/<int:pk>/add_student', AddStudent.as_view(), name='AddStudent'),
    path('courses/<int:pk>/remove_student', RemoveStudent.as_view(), name='RemoveStudent'),
    path('courses/<int:pk>/get_homework', GetHomework.as_view(), name='GetHomework'),

    path('students', StudentList.as_view(), name='StudentList'),
    path('students/<int:pk>', StudentDetail.as_view(), name='StudentDetail'),

    path('teachers', TeacherList.as_view(), name='TeacherList'),
    path('teachers/<int:pk>', TeacherDetail.as_view(), name='TeacherDetail'),

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
