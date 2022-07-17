"""smokers_predictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from .views import *
from .settings import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students', show_students, name='students'),
    path('signup', user_signup, name='signup'),
    path('test', show_test, name='test'),
    path('login', user_login, name='login'),
    path('test_result', show_test_result, name='test_result'),
    path('logout/', logout_view, name='logout'),
    path('login/', redirect_login),
    path('', redirect_login),
]
