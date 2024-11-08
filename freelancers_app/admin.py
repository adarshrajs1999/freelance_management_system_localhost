from django.contrib import admin
from .models import User, FreelancerProfile, CustomerProfile, Task, PaymentDetail, TaskSubmission


# Register User model (Django automatically registers the default User model, but if you want to customize it, you can create a custom admin class)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)


# Register FreelancerProfile model
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'communication_address', 'is_approved')
    search_fields = ('user__username', 'phone_number')


admin.site.register(FreelancerProfile, FreelancerProfileAdmin)


# Register CustomerProfile model
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'company_name', 'business_area')
    search_fields = ('user__username', 'company_name')


admin.site.register(CustomerProfile, CustomerProfileAdmin)


# Register Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_completed', 'deadline')
    search_fields = ('title', 'description')


admin.site.register(Task, TaskAdmin)


# Register PaymentDetail model
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'task', 'bank_account', 'is_paid')
    search_fields = ('freelancer__user__username', 'task__title')


admin.site.register(PaymentDetail, PaymentDetailAdmin)


# Register TaskSubmission model
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'task', 'submission_date')
    search_fields = ('freelancer__user__username', 'task__title')


admin.site.register(TaskSubmission, TaskSubmissionAdmin)
