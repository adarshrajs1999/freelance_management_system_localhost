# freelancers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Freelancer registration, login, and logout
    path('register/freelancer/', views.register_freelancer, name='register_freelancer'),
    path('login/freelancer/', views.freelancer_login, name='freelancer_login'),
    path('logout/freelancer/', views.freelancer_logout, name='freelancer_logout'),

    # Customer registration, login, and logout
    path('register/customer/', views.register_customer, name='register_customer'),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('logout/customer/', views.customer_logout, name='customer_logout'),

    # Dashboards
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    # Task management
    path('tasks/', views.view_tasks, name='task_list'),
    path('tasks/submit/<int:task_id>/', views.submit_task, name='submit_task'),

    # Payment details
    path('tasks/<int:task_id>/payment/', views.payment_details, name='payment_details'),
    path('customer/tasks/', views.customer_task_list, name='customer_task_list'),
    path('task/<int:task_id>/details/', views.task_detail_view, name='task_detail'),


]
