from django.urls import path
from apps.task import views

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('', views.home, name='home'),
    path('task/', views.task, name='task'),
    path('task_completed_list/', views.task_completed_list, name='task_completed_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/update/<int:task_id>/', views.task_edit, name='task_update'),
    path('task/detail/<int:task_id>/completed/', views.task_completed, name='task_completed'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]