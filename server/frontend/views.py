from django.shortcuts import render

# Create your views here.
# frontend/views.py

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import HomeworkForm

@csrf_exempt


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            response_data = {
                'message': 'Login successful',
                'access': csrf_token  # 返回新的 CSRF token
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def signup_view(request):
    return render(request, 'signup.html')

def teacher_info(request):
    return render(request, 'teacher_info.html')
def student_info(request):
    return render(request, 'student_info.html')

def course(request):
    return render(request, 'course-model.html')

from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Course, Teacher,Student
from .forms import CourseForm

def course_create_view(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            response_data = {
                'message': 'Course created successfully',
                'redirect_url': course.get_absolute_url()
            }
            return JsonResponse(response_data, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': 'Invalid data', 'details': errors}, status=400)
    else:
        form = CourseForm()
    return render(request, 'course_create.html', {'form': form})
	
def course_detail_view(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'course_detail.html', {'course': course})
	
def course_assignment_view(request, course_id, teacher_id):
    course = get_object_or_404(Course, id=course_id)
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'course_assignment.html', {'course': course, 'teacher': teacher})
	
def course_assignment_student_view(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'course_assignment_student.html', {'course': course, 'student': student})



from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import HomeworkForm
from accounts.models import Course, Teacher,Homework

def course_assignment_create_view(request, course_id, teacher_id):
    course = get_object_or_404(Course, id=course_id)
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.course = course
            homework.teacher = teacher
            homework.save()
            return JsonResponse({'message': 'Assignment submitted successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Form is not valid', 'errors': form.errors}, status=400)
    else:
        form = HomeworkForm()
    
    return render(request, 'course_assignment_create.html', {'form': form, 'course': course, 'teacher': teacher})
	
def homework_detail_teacher_view(request, homework_id,teacher_id):
    print(homework_id)
    homework = get_object_or_404(Homework, id=homework_id)
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'homework_detail.html', {'homework': homework,'teacher': teacher})

def homework_detail_student_view(request,course_id, homework_id,student_id):
    course = get_object_or_404(Course, id=course_id)
    homework = get_object_or_404(Homework, id=homework_id)
    student = get_object_or_404(Teacher, id=student_id)
    return render(request, 'homework_detail.html', {'course': course,'homework': homework,'student': student})
	

import requests
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .forms import SubmissionForm
from accounts.models import Submission

def grade_homework(url, ti_mu, ping_fen, zuo_ye):
    messages = [
        {
            "role": "user",
            "content": "你现在需要作为助教，帮我批阅学生的作业，我会给你题目要求，评分细则，以及学生的作业，请你给出一个详细的评价，指出学生作业中的不足，并给出参考分数。" +
                       "题目要求：" + ti_mu +
                       "评分细则：" + ping_fen +
                       "学生提交的作业：" + zuo_ye +
                       "请指出学生作业中的不足，并给出参考分数。"
        }
    ]
    data = {
        "model": "yi:34b",
        "messages": messages,
        "stream": False
    }
    try:
        r = requests.post('http://' + url + '/api/chat', json=data)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return {"comment": "", "score": 0, "message": "无法获取评分，请稍后重试。"}

@csrf_exempt
def submit_homework(request):
    if request.method == 'POST':
        print(request.POST)  # 打印接收到的表单数据
        form = SubmissionForm(request.POST)
        if form.is_valid():
            try:
                submission = form.save(commit=False)
                file_content = submission.content
                ti_mu = submission.homework.content
                ping_fen = "请根据学生作业内容进行评分，满分100分；"
                feedback_response = grade_homework('ollama.gujialiang123.top', ti_mu, ping_fen, file_content)
                submission.time=feedback_response.get('created_at','')
                submission.comment = feedback_response.get('comment', '')
                submission.score = feedback_response.get('score', 0)
                submission.feedback = feedback_response.get('message', '')
                submission.save()
                return JsonResponse({
                    'success': True,
                    'submission': {
                        'id': submission.pk,
                        'comment': submission.comment,
                        'score': submission.score,
                        'feedback': submission.feedback,
                        'student': submission.student.name,
                        'homework': submission.homework.id
                    }
                })
            except Exception as e:
                print(f"Error while saving submission: {e}")
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            print("表单验证错误:", form.errors)  # 打印表单错误信息
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return HttpResponseBadRequest("无效的请求方法")

def submission_detail(request, pk,homework_id,course_id,student_id):
    homework = get_object_or_404(Homework, id=homework_id)
    student = get_object_or_404(Teacher, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    submission = Submission.objects.get(pk=pk)
    return render(request, 'submission_detail.html', {'submission': submission,'course': course,'homework': homework,'student': student})

def courses(request):

    return render(request, 'courses.html')
	
def submission_list(request,course_id,homework_id,student_id):
    homework = get_object_or_404(Homework, id=homework_id)
    student = get_object_or_404(Teacher, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'submission_list.html', {'course': course,'homework': homework,'student': student})

def submission_list_teacher(request,course_id,homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'submission_list_teacher.html', {'course': course,'homework': homework})
