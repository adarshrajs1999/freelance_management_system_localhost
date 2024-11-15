# freelancers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission
from .forms import (
    UserRegistrationForm,
    FreelancerProfileForm,
    CustomerRegistrationForm,
    TaskSubmissionForm,
    UserEditForm,
    FreelancerProfileEditForm,
    CustomerProfileEditForm,
    PasswordUpdateForm
)


def home(request):
    return render(request, "home.html")


def register_user(request, user_form_class, profile_form_class=None, role=None, redirect_url=None, template_name=None):
    if request.method == 'POST':
        user_form = user_form_class(request.POST)
        profile_form = profile_form_class(request.POST, request.FILES) if profile_form_class else None
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user = user_form.save(commit=False)
            user.role = role
            user.save()
            if profile_form:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            messages.success(request, f"{role.capitalize()} registration successful! Please log in.")
            return redirect(redirect_url)
    else:
        user_form = user_form_class()
        profile_form = profile_form_class() if profile_form_class else None
    return render(request, template_name, {'user_form': user_form, 'profile_form': profile_form})


def register_freelancer(request):
    return register_user(
        request,
        user_form_class=UserRegistrationForm,
        profile_form_class=FreelancerProfileForm,
        role='freelancer',
        redirect_url='freelancer_login',
        template_name='register_freelancer.html'
    )


def register_customer(request):
    return register_user(
        request,
        user_form_class=CustomerRegistrationForm,
        role='viewer',
        redirect_url='customer_login',
        template_name='register_customer.html'
    )


def login_view(request):
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.role == 'freelancer' and not FreelancerProfile.objects.get(user=user).is_approved:
                messages.error(request, "Your account is not approved by the admin yet.")
            else:
                login(request, user)
                return redirect('freelancer_task_list' if user.role == 'freelancer' else 'customer_task_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


@login_required
def freelancer_task_list(request):
    tasks = Task.objects.filter(is_completed=False)
    return render(request, 'freelancer_task_list.html', {'tasks': tasks})


@login_required
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role != 'freelancer':
        return redirect('home')
    freelancer_profile = FreelancerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            task_submission = form.save(commit=False)
            task_submission.freelancer = freelancer_profile
            task_submission.task = task
            task_submission.save()
            task.is_completed = True
            task.save()
            return redirect('freelancer_task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'submit_task.html', {'form': form, 'task': task})


@login_required
def customer_task_list(request):
    tasks = Task.objects.filter(is_completed=False)
    return render(request, 'customer_task_list.html', {'tasks': tasks})


def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def edit_profile(request, profile_class, user_form_class, profile_form_class, template_name, redirect_url):
    profile, _ = profile_class.objects.get_or_create(user=request.user)
    user_form = user_form_class(instance=request.user)
    profile_form = profile_form_class(instance=profile)
    password_form = PasswordUpdateForm(user=request.user)

    if request.method == 'POST':
        user_form = user_form_class(request.POST, instance=request.user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=profile)
        password_form = PasswordUpdateForm(request.user, request.POST)
        if all(form.is_valid() for form in [user_form, profile_form, password_form]):
            user_form.save()
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Your profile has been updated successfully!")
            return redirect(redirect_url)

    return render(request, template_name, {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })


@login_required
def edit_freelancer_profile(request):
    return edit_profile(
        request,
        profile_class=FreelancerProfile,
        user_form_class=UserEditForm,
        profile_form_class=FreelancerProfileEditForm,
        template_name='edit_freelancer_profile.html',
        redirect_url='edit_freelancer_profile'
    )


@login_required
def edit_customer_profile(request):
    return edit_profile(
        request,
        profile_class=CustomerProfile,
        user_form_class=UserEditForm,
        profile_form_class=CustomerProfileEditForm,
        template_name='edit_customer_profile.html',
        redirect_url='edit_customer_profile'
    )


def forgot_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_mail(
                'Your Username',
                f'Hello {user.username},\n\nYour username is: {user.username}',
                'your-email@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Your username has been sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
    return render(request, 'forgot_username.html')
