# freelancers/models.py
from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('freelancer', 'Freelancer'),
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"  # Display username and role


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer_profile")
    phone_number = models.CharField(max_length=15)
    communication_address = models.CharField(max_length=500)
    resume = models.FileField(upload_to='resumes/')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Freelancer Profile - {self.phone_number}"  # Add phone number


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    communication_address = models.CharField(max_length=500)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    business_area = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile - {self.company_name or 'No Company'}"  # Show company name if available


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    payment_amount = models.PositiveIntegerField(default=0)
    file_upload = models.FileField(upload_to='task_documents/', null=True, blank=True)
    task_url = models.URLField(max_length=200, null=True, blank=True)  # New field for task URL

    def __str__(self):
        return f"{self.title} - Deadline: {self.deadline if self.deadline else 'No Deadline'}"  # Show deadline if present




class TaskSubmission(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='task_submissions')  # Changed related_name to 'task_submissions'
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_submissions')  # Changed related_name to 'task_submissions'
    git_link = models.URLField(max_length=200)
    file_upload = models.FileField(upload_to='task_submissions/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.freelancer.user.username} for task: {self.task.title} on {self.submission_date.strftime('%Y-%m-%d %H:%M:%S')}"
