# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Submission
from .forms import FreelancerRegisterForm, SubmissionForm


def home(request):
    return render(request,'home.html')


def register(request):
    if request.method == 'POST':
        form = FreelancerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = FreelancerRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def submit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.freelancer = request.user
            submission.task = task
            submission.save()
            return redirect('task_list')
    else:
        form = SubmissionForm()
    return render(request, 'submit_task.html', {'form': form, 'task': task})
