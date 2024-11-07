from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('freelancer', 'Freelancer'),
        ('viewer', 'Viewer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='viewer')
    phone_number = models.CharField(max_length=15, blank=True)
    communication_address = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_tasks')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentDetails(models.Model):
    freelancer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_details')
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    google_pay_number = models.CharField(max_length=15, blank=True)
    phone_pe_number = models.CharField(max_length=15, blank=True)