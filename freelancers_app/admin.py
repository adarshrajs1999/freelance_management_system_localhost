from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission, Customer_Task, TaskApplication


# Custom User Admin to manage the User model
class UserAdmin(BaseUserAdmin):
    # Use Django’s built-in AdminPasswordChangeForm for password editing
    change_password_form = AdminPasswordChangeForm

    # Fields to display in the admin list view
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('role',)

    # Fields to include in the edit form in admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Information', {'fields': ('role',)}),
    )

    # Fields to include when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'email'),
        }),
    )

    # Password change form functionality
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['password'].required = False
        return form


class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'task', 'git_link', 'file_upload', 'description', 'submission_date')
    readonly_fields = ('task', 'freelancer')  # Make 'task' and 'freelancer' fields read-only


admin.site.register(TaskSubmission, TaskSubmissionAdmin)




# Register models with the custom admin classes
admin.site.register(User, UserAdmin)



admin.site.register(Task)


class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'communication_address', 'is_approved')
    readonly_fields = ('user',)  # Make 'user' field read-only



admin.site.register(FreelancerProfile, FreelancerProfileAdmin)


class CustomerProfileAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin panel
    list_display = ('user', 'phone_number', 'company_name', 'business_area','communication_address')

    # Make the 'user' field read-only
    readonly_fields = ('user',)



# Register the model with the custom admin
admin.site.register(CustomerProfile, CustomerProfileAdmin)

from django.contrib import admin
from .models import Customer_Task


class CustomerTasksAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin interface
    list_display = (
    'customer', 'work_category',  'deadline',  'payment_amount', 'file_upload')

    # Specify which fields are read-only
    readonly_fields = ('customer',)

    # Optionally, you can exclude the customer field from the form (if you don't want to show it in the form at all)
    # exclude = ('customer',)

    # Optionally, you can also customize the form layout
    # fields = ('customer', 'title', 'description', 'deadline', 'is_approved', 'is_completed', 'payment_amount', 'file_upload', 'task_url')


admin.site.register(Customer_Task, CustomerTasksAdmin)


class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'task', 'status', 'applied_on')
    readonly_fields = ('task', 'freelancer')  # Make 'task' and 'freelancer' fields read-only


admin.site.register(TaskApplication, TaskApplicationAdmin)