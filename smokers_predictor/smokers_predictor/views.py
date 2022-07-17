from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from .models import *
from .services import *


def redirect_login(request):
    return HttpResponseRedirect(reverse('login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('students'))
            else:
                return HttpResponse('Неверный логин или пароль!')
    else:
        form = LoginForm()
    return render(request, 'smokers_predictor/user_login.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = save_user(user_form)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('students'))
            else:
                return HttpResponse('Такой e-mail уже занят!')
    else:
        user_form = RegisterForm()
    return render(request, 'smokers_predictor/signup.html', {'user_form': user_form})


@login_required
def show_students(request):
    if request.method == "GET":
        form = FilterForm(request.GET)
        data = get_students_data(request)
        return render(request, 'smokers_predictor/students.html', {'data': data, 'form': form})


def show_test(request):
    if request.method == "GET":
        return render(request, 'smokers_predictor/index.html')


@csrf_exempt
def show_test_result(request):
    if request.method == "POST":
        prediction = predict(request)
        if request.user.is_authenticated:
            student = save_student(request)
            save_exam(prediction, student)
        return HttpResponseRedirect("%s?result=%s" % (reverse('test_result'), str(prediction)))
    else:
        return render(request, 'smokers_predictor/test_result.html', {'probability': request.GET.get('result', None)})
