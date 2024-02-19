from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

from django import forms 

class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "email", "username", "password1", "password2")
        labels={
            "first_name": "Name",
            "username": "Student number",
            "email": "AUT email address"
        }


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"



class LoginForm(AuthenticationForm):
    username = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={
                    "type": "username",
                    "placeholder": "Student Number",
                }
            ),
        )


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

