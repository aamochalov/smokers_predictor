''' Функции для работы с БД и нейросетью '''

import numpy as np
from keras.models import load_model
from datetime import datetime
from .models import *
from .forms import RegisterForm


model = load_model("smokers_predictor/smokers_predictor/predictor.h5")
questions_startpoints = [0, 2, 4, 6, 8, 11, 13, 16, 20, 22, 25]


def get_students_data(request):
    teacher = Teacher.objects.filter(email=request.user.email)[:1][0]
    students = Student.objects.filter(teacher=teacher)

    fio = request.GET.get("fio", None)
    cl_num = request.GET.get("cl_num", None)
    cl_let = request.GET.get("cl_let", None)
    date_sort = request.GET.get("date_sort", None)

    data = []
    for student in students:
        if fio and str(student.name).find(fio) == -1:
            continue
        if cl_num and cl_num != "0" and str(student.class_num) != cl_num:
            continue
        if cl_let and cl_let != "0" and str(student.class_letter) != cl_let:
            continue

        exams = Exam.objects.filter(student=student)
        for exam in exams:
            data.append([])
            data[-1].append(str(student.name))
            data[-1].append(str(student.class_num))
            data[-1].append(str(student.class_letter))
            data[-1].append(str(exam.date))
            data[-1].append(str(exam.result) + "%")

    if date_sort and date_sort == "2":
        data.sort(key=lambda student: datetime.strptime(student[3], '%Y-%m-%d'), reverse=True)

    return data


def save_user(user_form: RegisterForm):
    cd = user_form.cleaned_data
    teachers = Teacher.objects.filter(email=cd['email'])
    if teachers.count() == 0:
        new_user = user_form.save(commit=False)
        new_user.set_password(cd['password'])
        new_user.save()
        teacher = Teacher(name=cd['first_name'], email=cd['email'], school=cd['school'])
        teacher.save()
        return new_user
    return None


def save_student(request):
    fio=request.POST.get("fio", None)
    cl_num=int(request.POST.get("cl_num", None))
    cl_let=request.POST.get("cl_let", None)
    teacher = Teacher.objects.filter(email=request.user.email)[:1][0]

    students = Student.objects.filter(name=fio, class_num=cl_num, class_letter=cl_let, teacher=teacher)
    if students.count() != 0:
        return students[:1][0]
    else:
        student = Student(name=fio, class_num=cl_num, class_letter=cl_let, teacher=teacher)
        student.save()
    return student


def save_exam(result: float, student: Student):
    exam = Exam(result=result, student=student)
    exam.save()


def predict(request):
    data = prepare_data(request)
    prediction = model.predict(data)
    result = round(prediction[0, 0] * 100, 2)
    return result


def prepare_data(request):
    data = np.empty([1, 25])
    for question in range(1, 11):
        answer = int(request.POST.get("q" + str(question), None))
        for data_index in range(questions_startpoints[question] - questions_startpoints[question - 1]):
            if answer == data_index + 1:
                data[0, questions_startpoints[question - 1] + data_index] = 1
            else:
                data[0, questions_startpoints[question - 1] + data_index] = 0
    return data
