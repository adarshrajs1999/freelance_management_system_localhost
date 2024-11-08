# freelancers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, FreelancerProfile, Task, PaymentDetail
from .forms import UserRegistrationForm, FreelancerProfileForm, CustomerRegistrationForm, TaskForm, PaymentDetailForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, "home.html")


# Freelancer registration view
def register_freelancer(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = FreelancerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'freelancer'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Freelancer registration successful! Please log in.")
            return redirect('freelancer_login')
    else:
        user_form = UserRegistrationForm()
        profile_form = FreelancerProfileForm()
    return render(request, 'register_freelancer.html', {'user_form': user_form, 'profile_form': profile_form})


# Customer registration view
def register_customer(request):
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'viewer'  # Set role as viewer for customers
            user.save()
            messages.success(request, "Customer registration successful! Please log in.")
            return redirect('customer_login')
    else:
        user_form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'user_form': user_form})


# Freelancer login view
def freelancer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'freelancer':
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('freelancer_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'user_type': 'freelancer'})


# Customer login view
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'viewer':
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'user_type': 'customer'})


# Freelancer logout view
@login_required
def freelancer_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('freelancer_login')


# Customer logout view
@login_required
def customer_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('customer_login')


# Freelancer dashboard view
@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('home')
    return render(request, 'freelancer_dashboard.html')


# Customer dashboard view
@login_required
def customer_dashboard(request):
    if request.user.role != 'viewer':
        return redirect('home')
    tasks = Task.objects.filter(is_completed=False)
    return render(request, 'customer_dashboard.html', {'tasks': tasks})


# Freelancer views tasks
@login_required
def view_tasks(request):
    if request.user.role != 'freelancer':
        return redirect('home')
    tasks = Task.objects.filter(is_completed=False, assigned_to=None)
    return render(request, 'task_list.html', {'tasks': tasks})


# Freelancer submits task completion
@login_required
def submit_task(request, task_id):
    if request.user.role != 'freelancer':
        return redirect('home')
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user.freelancer_profile)
    if request.method == 'POST':
        task.is_completed = True
        task.save()
        messages.success(request, "Task submitted successfully!")
        return redirect('task_list')
    return render(request, 'submit_task.html', {'task': task})


# Freelancer payment form
@login_required
def payment_details(request, task_id):
    if request.user.role != 'freelancer':
        return redirect('home')
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user.freelancer_profile)
    if request.method == 'POST':
        form = PaymentDetailForm(request.POST)
        if form.is_valid():
            payment_detail = form.save(commit=False)
            payment_detail.freelancer = request.user.freelancer_profile
            payment_detail.task = task
            payment_detail.save()
            messages.success(request, "Payment details submitted!")
            return redirect('task_list')
    else:
        form = PaymentDetailForm()
    return render(request, 'payment_form.html', {'form': form})
