"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
     path('api/', include('students.urls')),
]

from django.http import JsonResponse
import jwt

def validate_token(token):
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=['HS256']) # Decode without verifying signature
        print(decoded_token)  # Print token contents for debugging
        if 'id' in decoded_token:
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False

def protected_view(request):
    if 'Authorization' not in request.headers:
        return JsonResponse({'error': 'Authorization header missing'}, status=401)

    token = request.headers['Authorization'].split(' ')[1]  # Extract token from Authorization header
    if validate_token(token):
        # Token is valid, allow access to protected resource
        return JsonResponse({'message': 'Access granted'})
    else:
        # Token is not valid, deny access
        return JsonResponse({'error': 'Invalid token'}, status=401)

