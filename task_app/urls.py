from django.urls import path
from task_app import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project-create'),
    
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
]
