from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register_freelancer, name='register_freelancer'),
    path('tasks/', views.task_list, name='task_list'),
    path('submit_task/<int:task_id>/', views.submit_task, name='submit_task'),
    # Add other paths here
]