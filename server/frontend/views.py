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

def user(request):
    return render(request, 'user.html')

def course(request):
    return render(request, 'course-model.html')

from django.utils import timezone

def your_view(request):
    context = {
        'timestamp': int(timezone.now().timestamp())
    }
    return render(request, 'your_template.html', context)
