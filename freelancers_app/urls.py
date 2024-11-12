# freelancers/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views





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

    # Task management
    path('freelancer_task_list/', views.freelancer_task_list, name='freelancer_task_list'),
    path('tasks/submit/<int:task_id>/', views.submit_task, name='submit_task'),

    path('customer/tasks/', views.customer_task_list, name='customer_task_list'),
    path('task/<int:task_id>/details/', views.task_detail_view, name='task_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_freelancer_profile/', views.edit_freelancer_profile, name='edit_freelancer_profile'),
    path('edit_customer_profile/', views.edit_customer_profile, name='edit_customer_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('forgot_username/', views.forgot_username, name='forgot_username'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
