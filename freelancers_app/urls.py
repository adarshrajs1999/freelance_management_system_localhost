from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import create_customer_task

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),

    # Registration
    path('register/freelancer/', views.register_freelancer, name='register_freelancer'),
    path('register/customer/', views.register_customer, name='register_customer'),

    # Profile Editing
    path('edit/freelancer/profile/', views.edit_freelancer_profile, name='edit_freelancer_profile'),
    path('edit/customer/profile/', views.edit_customer_profile, name='edit_customer_profile'),

    # Task Management (Freelancer and Customer)
    path('freelancer/tasks/', views.freelancer_task_list, name='freelancer_task_list'),
    path('tasks/submit/<int:task_id>/', views.submit_task, name='submit_task'),
    path('customer/create-task/', create_customer_task, name='create_customer_task'),
    path('task/<int:task_id>/details/', views.task_detail_view, name='task_detail'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    # Username Retrieval
    path('forgot_username/', views.forgot_username, name='forgot_username'),
    path('apply/<int:task_id>/', views.apply_for_task, name='apply_for_task'),
    path('task/update/<int:task_id>/', views.update_task, name='update_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('terms_and_conditions/',views.terms_and_conditions,name='terms_and_conditions')



]
