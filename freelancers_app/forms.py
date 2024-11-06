# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Submission

class FreelancerRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['git_link', 'file_upload']
