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
        fields = ['company_name', 'business_area']


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
        exclude = ['customer', 'is_approved', 'is_completed']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'payment_amount': forms.NumberInput(attrs={'step': '1'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'deadline': 'Deadline',
            'payment_amount': 'Payment Amount (Rs.)',
            'file_upload': 'Upload File (Optional)',
            'task_url': 'Task URL (Optional)',
        }

