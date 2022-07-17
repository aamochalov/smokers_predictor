from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Teacher(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=60)
    class_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)])
    class_letter = models.CharField(max_length=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('name', 'class_num', 'class_letter', 'teacher')


class Exam(models.Model):
    date = models.DateField(auto_now=True)
    result = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
