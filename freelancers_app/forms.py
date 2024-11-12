# freelancers/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FreelancerProfile, Task
from .models import TaskSubmission


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['phone_number', 'communication_address', 'resume']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']



class FreelancerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    communication_address = forms.CharField(widget=forms.Textarea, required=True)
    resume = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone_number', 'communication_address', 'resume']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'freelancer'
        if commit:
            user.save()
            FreelancerProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                communication_address=self.cleaned_data['communication_address'],
                resume=self.cleaned_data['resume'],
            )
        return user

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'viewer'  # Set the role to 'viewer' for customer accounts
        if commit:
            user.save()
        return user





class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['git_link', 'file_upload','description']

    # freelancers/forms.py


from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, FreelancerProfile, CustomerProfile


# Form to edit user info (username, email, and password)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class FreelancerProfileEditForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['phone_number', 'communication_address', 'resume']


class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['company_name', 'business_area']


# Form for updating password
class PasswordUpdateForm(PasswordChangeForm):
    pass
