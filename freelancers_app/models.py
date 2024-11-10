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

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer_profile")
    phone_number = models.CharField(max_length=15)
    communication_address = models.CharField(max_length=500)
    resume = models.FileField(upload_to='resumes/')
    is_approved = models.BooleanField(default=False)



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    communication_address = models.CharField(max_length=500)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    business_area = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"



class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    payment_amount = models.PositiveIntegerField(default=0)  # New field added
    file_upload = models.FileField(upload_to='task_documents/', null=True, blank=True)


    def __str__(self):
        return self.title



class PaymentDetail(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    bank_account = models.CharField(max_length=50)
    gpay_number = models.CharField(max_length=15, blank=True, null=True)
    phonepe_number = models.CharField(max_length=15, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Detail for Task {self.task.title} by {self.freelancer.user.username}"



class TaskSubmission(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='submissions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    git_link = models.URLField(max_length=200)
    file_upload = models.FileField(upload_to='task_submissions/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # New text field
    submission_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Submission by {self.freelancer.user.username} for task: {self.task.title}"