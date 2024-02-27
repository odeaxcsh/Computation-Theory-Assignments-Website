from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

from django.contrib.staticfiles import finders


from django import forms 

import csv



class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) ->  None:
        super().__init__(*args, **kwargs)
        filepath = finders.find('participants.csv')
        csvfile = csv.reader(open(filepath, 'r'), delimiter=',')
        self.participants = dict(row for row in csvfile)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "email", "username", "password1", "password2")
        labels={
            "username": "Student number as your username",
            "first_name": "Name",
            "email": "AUT email address"
        }

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        username = cleaned_data.get('username')
        email = self.participants.get(username)
        if email is None:
            self.add_error('username', 'Your student number is not registered. Contact website admin')

        if email is not None and email != cleaned_data.get('email'):
            self.add_error('email', 'Email is different from your email in Courses')
        
        return cleaned_data


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserLoginView(LoginView):
    template_name = "registration/login.html"

