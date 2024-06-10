# accounts/views.py

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound

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
            404:
            - error: ='Student or Course not found'
        '''
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise NotFound('Course not found')

        # 打印请求数据
        print(request.data)

        student_id = request.data.get('student')

        # 打印 student_id
        print(f'student_id: {student_id}')

        if not student_id:
            return Response({'error': 'Student ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')

        course.student.add(student)  # 假设你的Course模型中有一个名为students的ManyToManyField
        return Response({'status': 'student added'}, status=status.HTTP_200_OK)

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
	
	
	
	

class FileList(generics.ListAPIView):
    # only use for debug
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer


class FileUpload(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    '''
    Upload a file, return its id.
    '''
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer


class FileDownload(APIView):
    def get_object(self, pk):
        try:
            return FileModel.objects.get(pk=pk)
        except FileModel.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        '''
        Download file by file id, return a file.
        '''
        file_obj = self.get_object(pk)
        return FileResponse(open(file_obj.file.path, 'rb'))

class HomeworkList(generics.ListCreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class HomeworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class GetHomework(APIView):
    def get(self, request, pk):
        '''
        Return a list of all homeworks of a course.

        - **Responses**:

            500:
            - id: int, homework id
            - name: string, homework name
            - description: string, homework description
            - course: int, course id of homework
            - file: int, file id of homework
        '''
        homework = Homework.objects.filter(course__id=pk)
        serializer = HomeworkSerializer(homework, many=True)
        return Response(serializer.data)


class SubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class GetAllSubmission(APIView):
    def get(self, request, pk):
        '''
        Return a list of all submissions in a homework.

        - **Responses**:

            500:
            - id: int, submission id
            - comment: string, submission comment
            - student: int, student id of submission
            - homework: int, homework id of submission
            - file: int, file id of submission
        '''
        result = Submission.objects.filter(homework__id=pk)
        serializer = SubmissionSerializer(result, many=True)
        return Response(serializer.data)
    

class GetSubmission(APIView):
    def get(self, request, pk):
        '''
        Return a list of all submissions of a student in a homework.

        - **Query Parameters**:

            student: int, student id

        - **Responses**:

            500:
            - id: int, submission id
            - comment: string, submission comment
            - student: int, student id of submission
            - homework: int, homework id of submission
            - file: int, file id of submission
        '''
        student = request.query_params.get('student', None)
        result = Submission.objects.filter(homework__id=pk, student__id=student)
        serializer = SubmissionSerializer(result, many=True)
        return Response(serializer.data)
	
	
	
	
	
	
	
	
	


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


