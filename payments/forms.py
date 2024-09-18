from django import forms

from .models import Payment

from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentSignUpForm(UserCreationForm):
    matric_number = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'matric_number', 'department']


class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['session']

