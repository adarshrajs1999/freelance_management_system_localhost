# freelancers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, FreelancerProfile, Task, PaymentDetail, TaskSubmission
from .forms import UserRegistrationForm, FreelancerProfileForm, CustomerRegistrationForm, TaskForm, PaymentDetailForm, \
    TaskSubmissionForm
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


def freelancer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'freelancer':
            # Check if freelancer is approved
            freelancer_profile = FreelancerProfile.objects.get(user=user)
            if not freelancer_profile.is_approved:
                messages.error(request, "You are not approved by the admin yet.")
                return render(request, 'login.html', {'user_type': 'freelancer'})

            # If approved, log in the user
            login(request, user)
            return redirect('freelancer_task_list')
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
            return redirect('customer_task_list')
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


@login_required
def freelancer_task_list(request):
    # Tasks that are not completed and have no submissions
    tasks = Task.objects.filter(is_completed=False)
    return render(request, 'freelancer_task_list.html', {'tasks': tasks})



def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Ensure only freelancers can submit tasks
    if request.user.role != 'freelancer':
        return redirect('home')

    freelancer_profile = FreelancerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the task submission
            task_submission = form.save(commit=False)
            task_submission.freelancer = freelancer_profile
            task_submission.task = task
            task_submission.save()

            # Mark the task as completed
            task.is_completed = True
            task.save()  # Save the task after updating the is_completed field

            # Redirect to the freelancer task list after submission
            return redirect('freelancer_task_list')
    else:
        form = TaskSubmissionForm()

    return render(request, 'submit_task.html', {'form': form, 'task': task})




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

@login_required
def customer_task_list(request):
    # Only display tasks that are not completed
    tasks = Task.objects.filter(is_completed=False)
    return render(request, 'customer_task_list.html', {'tasks': tasks})


def task_detail_view(request, task_id):
    # Fetch the task or return a 404 if it doesn't exist
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logging out