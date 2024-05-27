# accounts/views.py

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from .models import Course, Student, Teacher
from .serializers import CourseSerializer, StudentSerializer, TeacherSerializer


class RegisterView(generics.CreateAPIView):
    '''
    post:
    Register a new user, return username.

    '''
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class LoginView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        '''
        User login, return refresh token, access token and user id.

        ---
        - **Parameters**:

            username: string
            password: string

        - **Responses**:

            200:
            - refresh: string, refresh token
            - access: string, access token
            - user: int, user id

            400:
            - error: string, ="Invalid credentials"
        '''
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user.id
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class AddStudent(APIView):
    def post(self, request, pk):
        '''
        Add student, return status of success.

        ---
        - **Parameters**:

            student: int, student id

        - **Responses**:

            200:
            - status: ='student added'
        '''
        course = Course.objects.get(id=pk)
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        course.student.add(student)
        return Response({'status':'student added'}, status=status.HTTP_200_OK)
    
class RemoveStudent(APIView):
    def post(self, request, pk):
        '''
        Remove student, return status of success.

        ---
        - **Parameters**:

            student: int, student id

        - **Responses**:

            200:
            - status: ='student removed'
        '''
        course = Course.objects.get(id=pk)
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        course.student.remove(student)
        return Response({'status':'student removed'}, status=status.HTTP_200_OK)

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_login_status(request):
    if request.user.is_authenticated:
        return Response({
            'logged_in': True,
            'username': request.user.username
        })
    else:
        return Response({
            'logged_in': False
        }, status=status.HTTP_403_FORBIDDEN)
