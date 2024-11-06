# freelancer_project/urls.py

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/submit/', views.submit_task, name='submit_task'),
    path('logout/', views.custom_logout, name='logout'),  # Custom logout URL

]
