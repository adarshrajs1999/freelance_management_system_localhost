# freelancers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission, TaskApplication
from .forms import (
    UserRegistrationForm,
    FreelancerProfileForm,
    CustomerRegistrationForm,
    TaskSubmissionForm,
    UserEditForm,
    FreelancerProfileEditForm,
    CustomerProfileEditForm,
    PasswordUpdateForm, CustomerProfileForm, TaskForm
)
from django.shortcuts import get_object_or_404, redirect
from .models import Task, TaskApplication
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerTaskForm
from .models import Customer_Task




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
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = FreelancerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Save user form without committing to the database yet
            user = user_form.save(commit=False)
            user.role = 'freelancer'  # Set the role to 'freelancer' for the freelancer user
            user.save()

            # Save the freelancer profile linked to the user
            profile = profile_form.save(commit=False)
            profile.user = user  # Link the profile to the newly created user
            profile.save()

            # Send a success message after successful registration
            messages.success(request, "Freelancer registration successful! Please log in.")
            return redirect('login_view')  # Redirect to the login page after successful registration
    else:
        user_form = UserRegistrationForm()
        profile_form = FreelancerProfileForm()

    # Render the registration page with the forms
    return render(request, 'register_freelancer.html', {'user_form': user_form, 'profile_form': profile_form})



def register_customer(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'viewer'  # Set the role to 'viewer' for customers
            user.save()

            # Save the customer profile linked to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Customer registration successful! Please log in.")
            return redirect('login_view')
    else:
        user_form = UserRegistrationForm()
        profile_form = CustomerProfileForm()

    return render(request, 'register_customer.html', {'user_form': user_form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            # Check if the user is a staff member (Django admin)
            if user.is_staff:
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html')

            if user.role == 'freelancer':
                # Handle freelancer role
                if not FreelancerProfile.objects.get(user=user).is_approved:
                    messages.error(request, "Your account is not approved by the admin yet.")
                else:
                    login(request, user)
                    return redirect('freelancer_task_list')  # Redirect to freelancer task list if approved
            elif user.role == 'admin':
                # Handle admin role
                login(request, user)
                return redirect('admin_panel')  # Redirect to admin panel
            else:
                # For any other roles (you can customize this)
                login(request, user)
                return redirect('create_customer_task')  # Redirect to customer task creation page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')




@login_required
def freelancer_task_list(request):
    # Fetch tasks that are not completed (available tasks)
    tasks = Task.objects.filter(is_completed=False)

    # Get freelancer profile of the logged-in user
    freelancer = FreelancerProfile.objects.get(user=request.user)

    # Fetch all the applications by the freelancer
    applications = TaskApplication.objects.filter(freelancer=freelancer)

    # Map task ID to application status
    applied_tasks = {application.task.id: application.status for application in applications}

    # Fetch completed tasks for the freelancer (tasks that are marked as completed)
    completed_tasks = Task.objects.filter(
        taskapplication__freelancer=freelancer,
        is_completed=True
    )

    # Rendering the template with context
    return render(request, 'freelancer_dashboard.html', {
        'tasks': tasks,
        'applied_tasks': applied_tasks,  # Task IDs mapped to statuses
        'completed_tasks': completed_tasks,  # Tasks the freelancer has completed
    })




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




def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def logout_view(request):
    logout(request)
    return redirect('home')











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






@login_required
def create_customer_task(request):
    customer_profile = CustomerProfile.objects.get(user=request.user)
    tasks = Customer_Task.objects.filter(customer=customer_profile)
    if request.method == 'POST':
        form = CustomerTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.customer = customer_profile  # Assuming CustomerProfile is related to the User model
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('create_customer_task')  # Redirect to the customer's dashboard or success page
    else:
        form = CustomerTaskForm()

    return render(request, 'customer_dashboard.html', {'form': form,'tasks': tasks})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Task, TaskApplication, FreelancerProfile


@login_required
def apply_for_task(request, task_id):
    # Get the task object, raise 404 if not found
    task = get_object_or_404(Task, id=task_id)

    # Get the freelancer profile of the current user
    freelancer = FreelancerProfile.objects.get(user=request.user)

    try:
        # Check if the user has already applied for the task
        existing_application = TaskApplication.objects.get(task=task, freelancer=freelancer)

        if existing_application.status == 'Rejected':
            # Update the status to 'Pending' if it was rejected
            existing_application.status = 'Pending'
            existing_application.save()
        elif existing_application.status == 'Approved':
            # If already approved, inform the user (or handle accordingly)
            # You might want to show a message or prevent further action
            pass
        # Handle other statuses if necessary

    except TaskApplication.DoesNotExist:
        # If not applied yet, create a new application with status 'Pending'
        TaskApplication.objects.create(task=task, freelancer=freelancer, status='Pending')

    # Redirect to the task list or task details page
    return redirect('freelancer_task_list')  # Adjust the redirection as needed


def update_task(request, task_id):
    task = get_object_or_404(Customer_Task, id=task_id)
    if request.method == 'POST':
        form = CustomerTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('create_customer_task')  # Redirect to dashboard after update
    else:
        form = TaskForm(instance=task)

    return render(request, 'update_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Customer_Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('create_customer_task')  # Redirect to dashboard after deletion

def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')


@login_required
def edit_freelancer_profile(request):
    freelancer_profile = get_object_or_404(FreelancerProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)  # Edit the user data (like email, username)
        profile_form = FreelancerProfileEditForm(request.POST, request.FILES,
                                                 instance=freelancer_profile)  # Edit the freelancer profile

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the changes to the user
            profile_form.save()  # Save the changes to the freelancer profile
            messages.success(request, "Your freelancer profile has been updated successfully!")
            return redirect('edit_freelancer_profile')  # Or to any other page as necessary
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = FreelancerProfileEditForm(instance=freelancer_profile)

    return render(request, 'edit_freelancer_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def edit_customer_profile(request):
    customer_profile = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)  # Edit the user data (like email, username)
        profile_form = CustomerProfileEditForm(request.POST, request.FILES,
                                               instance=customer_profile)  # Edit the customer profile

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the changes to the user
            profile_form.save()  # Save the changes to the customer profile
            messages.success(request, "Your customer profile has been updated successfully!")
            return redirect('edit_customer_profile')  # Or to any other page as necessary
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = CustomerProfileEditForm(instance=customer_profile)

    return render(request, 'edit_customer_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
