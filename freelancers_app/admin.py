from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission, Customer_Tasks


# Custom User Admin to manage the User model
class UserAdmin(BaseUserAdmin):
    # Use Django’s built-in AdminPasswordChangeForm for password editing
    change_password_form = AdminPasswordChangeForm

    # Fields to display in the admin list view
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')

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


# Admin view for TaskSubmission
class TaskSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('freelancer',)

# Register models with the custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Task)
admin.site.register(TaskSubmission, TaskSubmissionAdmin)

# Register FreelancerProfile with the custom admin class
@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_approved')


# Register CustomerProfile with the custom admin class
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'business_area')

admin.site.register(Customer_Tasks)
