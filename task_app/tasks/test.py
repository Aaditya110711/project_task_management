from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_app.models import Project, Task
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone


class ProjectTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='password')

    def test_project_creation_valid(self):
        """Test project creation with valid dates."""
        project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            created_by=self.user
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.start_date, date(2024, 1, 1))
        self.assertEqual(project.end_date, date(2024, 12, 31))

    def test_end_date_validation(self):
        """Test that the end date can't be earlier than the start date."""
        with self.assertRaises(ValidationError):
            project = Project(
                name="Invalid Project",
                description="This project has invalid dates",
                start_date=date(2024, 1, 1),
                end_date=date(2023, 12, 31),
                created_by=self.user
            )
            project.full_clean()  # Will raise ValidationError if end date is earlier than start date


class TaskTestCase(TestCase):
    def setUp(self):
        # Create a test user and a project
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            created_by=self.user
        )

    def test_task_creation_valid(self):
        """Test task creation with valid dates."""
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            assigned_to=self.user,
            status="pending",
            priority="medium",
            start_date=date(2024, 1, 1),
            due_date=date(2024, 3, 31),
            project=self.project
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.due_date, date(2024, 3, 31))

    def test_task_due_date_exceeds_project_end_date(self):
        """Test that the task due date cannot exceed the project end date."""
        with self.assertRaises(ValidationError):
            task = Task(
                title="Invalid Task",
                description="This task has a due date beyond the project end date",
                assigned_to=self.user,
                status="pending",
                priority="medium",
                start_date=date(2024, 1, 1),
                due_date=date(2025, 1, 1),
                project=self.project
            )
            task.full_clean()  # Will raise ValidationError if task due date exceeds project end date


class ProjectDetailViewTestCase(TestCase):
    def setUp(self):
        # Create a user and a project
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            created_by=self.user
        )

    def test_project_detail_view(self):
        """Test that the project detail view shows the correct data."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('project-detail', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)


class TaskListViewTestCase(TestCase):
    def setUp(self):
        # Create a user and a project
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            created_by=self.user
        )
        # Create tasks for the user under the project
        self.task1 = Task.objects.create(
            title="Task 1",
            description="This is task 1",
            assigned_to=self.user,
            status="pending",
            priority="low",
            start_date=date(2024, 1, 1),
            due_date=date(2024, 2, 1),
            project=self.project
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="This is task 2",
            assigned_to=self.user,
            status="completed",
            priority="high",
            start_date=date(2024, 1, 1),
            due_date=date(2024, 3, 1),
            project=self.project
        )

    def test_task_list_view(self):
        """Test that the task list view shows all tasks for the user."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")

    def test_task_list_filter_by_status(self):
        """Test that the task list view can be filtered by task status."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('task-list') + '?status=pending')
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_task_list_filter_by_priority(self):
        """Test that the task list view can be filtered by priority."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('task-list') + '?priority=high')
        self.assertNotContains(response, "Task 1")
        self.assertContains(response, "Task 2")


class DashboardViewTestCase(TestCase):
    def setUp(self):
        # Create a user and a project
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            created_by=self.user
        )
        # Create some tasks for the user
        self.task1 = Task.objects.create(
            title="Task 1",
            description="This is task 1",
            assigned_to=self.user,
            status="pending",
            priority="low",
            start_date=date(2024, 1, 1),
            due_date=date(2024, 2, 1),
            project=self.project
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="This is task 2",
            assigned_to=self.user,
            status="completed",
            priority="high",
            start_date=date(2024, 1, 1),
            due_date=date(2024, 3, 1),
            project=self.project
        )

    def test_dashboard_view(self):
        """Test that the dashboard displays the user's projects and overdue tasks."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")
        self.assertNotContains(response, "No overdue tasks")
        # Test for overdue tasks (simulate overdue)
        self.task1.due_date = timezone.now().date() - timezone.timedelta(days=1)
        self.task1.save()
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "Task 1")  # Overdue task should show up
