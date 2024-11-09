from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm

# View for displaying a list of projects for a logged-in user
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'  # Template to render the project list
    context_object_name = 'projects'  # Context variable for the template

    # Custom queryset to filter projects based on the user's role (staff or not)
    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()  # Staff can see all projects
        return Project.objects.filter(created_by=self.request.user)  # Users can only see their own projects

# View for displaying the details of a specific project
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'  # Template to render project details

# View for creating a new project
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm  # Form to create a project
    template_name = 'tasks/project_form.html'  # Template for the form

    # Ensure the project is created by the logged-in user
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the user who created the project
        return super().form_valid(form)  # Proceed with the usual form submission

    # Handle form invalidity with a custom error message
    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your submission. Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

# View for updating an existing project
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm  # Form to update a project
    template_name = 'tasks/project_form.html'  # Template for the form

    # Restrict updating projects only to the creator of the project (if not staff)
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(created_by=self.request.user)  # User can only update their own projects
        return queryset

    # Handle form submission if valid
    def form_valid(self, form):
        return super().form_valid(form)

    # Handle form invalidity with a custom error message
    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your submission. Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

# View for listing tasks assigned to the logged-in user
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'  # Template to render the task list
    context_object_name = 'tasks'  # Context variable for the template

    # Custom queryset to filter tasks based on the user's role and filter options (status, priority)
    def get_queryset(self):
        queryset = Task.objects.all()  # Start with all tasks
        if not self.request.user.is_staff:
            queryset = queryset.filter(assigned_to=self.request.user)  # Users can only see tasks assigned to them

        # Filter tasks based on URL query parameters (status and priority)
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status:
            queryset = queryset.filter(status=status)  # Filter by task status
        if priority:
            queryset = queryset.filter(priority=priority)  # Filter by task priority

        return queryset

# View for creating a new task
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # Form to create a task
    template_name = 'tasks/task_form.html'  # Template for the form

    # Ensure the task's due date does not exceed the project's end date
    def form_valid(self, form):
        project = form.cleaned_data.get('project')  # Get the selected project from the form
        if project and form.cleaned_data['due_date'] > project.end_date:
            form.add_error(
                'due_date', "Task due date cannot exceed the project end date.")  # Custom validation error
            return self.form_invalid(form)  # Return invalid form if validation fails
        return super().form_valid(form)  # Proceed with the usual form submission

    # Handle form invalidity with a custom error message
    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your submission. Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

# View for displaying the details of a specific task
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'  # Template to render task details
    context_object_name = 'task'  # Context variable for the template

    # Restrict task visibility to the assigned user (unless the user is staff)
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(assigned_to=self.request.user)  # User can only see their own tasks
        return queryset

# View for updating an existing task
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm  # Form to update a task
    template_name = 'tasks/task_form.html'  # Template for the form

    # Restrict task update to the assigned user (unless staff)
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(assigned_to=self.request.user)  # User can only update their own tasks
        return queryset

    # Ensure the task's due date does not exceed the project's end date
    def form_valid(self, form):
        project = form.cleaned_data.get('project')  # Get the selected project from the form
        if project and form.cleaned_data['due_date'] > project.end_date:
            form.add_error(
                'due_date', "Task due date cannot exceed the project end date.")  # Custom validation error
            return self.form_invalid(form)  # Return invalid form if validation fails
        return super().form_valid(form)  # Proceed with the usual form submission

    # Handle form invalidity with a custom error message
    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your submission. Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

# Dashboard view to display an overview of the user's projects and overdue tasks
def dashboard(request):
    if not request.user.is_authenticated:  # Check if the user is logged in
        return redirect('login')  # Redirect to the login page if not authenticated

    context = {
        'projects': Project.objects.filter(created_by=request.user),  # Projects created by the logged-in user
        'overdue_tasks': Task.objects.filter(
            assigned_to=request.user,
            status__in=['pending', 'in_progress'],  # Filter tasks that are still pending or in progress
            due_date__lt=timezone.now().date()  # Filter overdue tasks
        ),
    }
    return render(request, 'tasks/dashboard.html', context)  # Render the dashboard template with the context data
