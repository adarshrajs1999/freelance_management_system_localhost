from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    # Custom email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email


class FreelancerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    communication_address = forms.CharField(widget=forms.Textarea, required=True)
    resume = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'freelancer'
        if commit:
            user.save()
            FreelancerProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                communication_address=self.cleaned_data['communication_address'],
                resume=self.cleaned_data['resume']
            )
        return user

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email')

        # Allow password to be the same as the email
        if password and email and password == email:
            return password  # Accept password as the same as email
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # Allow password to be the same as the email
        if username and email and username == email:
            return username  # Accept password as the same as email
        return username




class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'viewer'  # Set role to 'viewer' for customer accounts
        if commit:
            user.save()
        return user

    # Custom email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['phone_number', 'communication_address', 'resume']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone_number', 'communication_address', 'company_name','business_area']



class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['company_name', 'business_area','phone_number','communication_address']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']


class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['git_link', 'file_upload', 'description']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class FreelancerProfileEditForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['phone_number', 'communication_address', 'resume']


class PasswordUpdateForm(PasswordChangeForm):
    pass

# forms.py
from django import forms
from .models import Customer_Tasks

class CustomerTaskForm(forms.ModelForm):
    class Meta:
        model = Customer_Tasks
        exclude = ['customer', 'is_approved', 'is_completed']  # Exclude system-managed fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description', 'rows': 4}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'deadline': 'Deadline',
            'payment_amount': 'Payment Amount (Rs.)',
            'file_upload': 'Upload File (Optional)',

        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'payment_amount', 'file_upload', 'task_url']
