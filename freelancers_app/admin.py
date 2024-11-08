# freelancers/admin.py

from django.contrib import admin
from .models import User, FreelancerProfile, CustomerProfile, Task, PaymentDetail

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'phone_number')

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'business_area')
    search_fields = ('user__username', 'company_name', 'business_area')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('title', 'created_by__username')

@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'task', 'bank_account', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('freelancer__user__username', 'task__title')
