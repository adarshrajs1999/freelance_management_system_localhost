# freelancers/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FreelancerProfile, Task, PaymentDetail

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

class PaymentDetailForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = ['bank_account', 'gpay_number', 'phonepe_number']

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
