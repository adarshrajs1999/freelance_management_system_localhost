# freelancers/admin.py
from django.contrib import admin
from .models import User, FreelancerProfile, CustomerProfile, Task, TaskSubmission



admin.site.register(User)
admin.site.register(FreelancerProfile)
admin.site.register(CustomerProfile)
admin.site.register(Task)
admin.site.register(TaskSubmission)
