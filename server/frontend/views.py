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
from accounts.models import Course
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