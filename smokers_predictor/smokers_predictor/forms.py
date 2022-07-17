from django import forms
from django.contrib.auth.models import User
from numpy import False_


class FilterForm(forms.Form):
    CL_NUMS = (
        ('0', 'Любой'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')
    )

    CL_LETTERS = (
        ('0', 'Любая'), ('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'Е'), ('Ж', 'Ж'),
        ('З', 'З'), ('И', 'И'), ('К', 'К'), ('Л', 'Л'), ('М', 'М'), ('Н', 'Н'), ('О', 'О'),
        ('П', 'П'), ('Р', 'Р'), ('С', 'С'), ('Т', 'Т'), ('У', 'У'), ('Ф', 'Ф'), ('Х', 'Х'),
        ('Ц', 'Ц'), ('Ч', 'Ч'), ('Ш', 'Ш'), ('Ы', 'Ы'), ('Э', 'Э'), ('Ю', 'Ю'), ('Я', 'Я')
    )

    DATE_SORTS = (('1', 'Сначала старые'), ('2', 'Сначала новые'))

    fio = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Фамилия Имя Отчество', 'autofocus': True}), required=False)
    cl_num = forms.ChoiceField(label=False, widget=forms.Select, choices=CL_NUMS, required=False)
    cl_let = forms.ChoiceField(label=False, widget=forms.Select, choices=CL_LETTERS, required=False)
    date_sort = forms.ChoiceField(label=False, widget=forms.Select, choices=DATE_SORTS, required=False)



class LoginForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Имя пользователя', 'required': True, 'autofocus': True}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль', 'required': True}))


class RegisterForm(forms.ModelForm):
    school = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Название обр. учреждения', 'required': True}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль', 'required': True}))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите пароль', 'required': True}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {'username': False, 'first_name': False, 'email': False}
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Имя пользователя', 'required': True, 'autofocus': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Фамилия Имя Отчество', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'required': True})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']
