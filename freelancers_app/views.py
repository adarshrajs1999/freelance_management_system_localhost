from django.shortcuts import render, redirect
from .models import Task, PaymentDetails, User
from .forms import FreelancerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request,'home.html')

def register_freelancer(request):
    if request.method == 'POST':
        form = FreelancerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'freelancer'
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = FreelancerRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def task_list(request):
    if request.user.user_type == 'freelancer' or request.user.user_type == 'viewer':
        tasks = Task.objects.filter(assigned_to__isnull=True, is_approved=False)
        return render(request, 'task_list.html', {'tasks': tasks})
    return HttpResponseForbidden("You don't have permission to view this page.")

def submit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.user.user_type == 'freelancer':
        task.assigned_to = request.user
        task.save()
        return redirect('task_list')


