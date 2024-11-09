# Project Task Management System

A Django-based project management system that allows users to create and manage projects and tasks.

## Features

- User authentication and authorization
- Project management (create, read, update, delete)
- Task management with status tracking
- Dashboard with project overview
- Filtering tasks by status and priority

## Setup
1. Clone the repository:
```bash
git clone https://github.com/Aaditya110711/project_task_management.git
cd project_task_management
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
project_task_management/
│
├── manage.py
├── requirements.txt
│
├── project_task_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── task_app/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
└── templates/
    ├── registration/
    │   └── login.html
    └── tasks/
        ├── base.html
        ├── dashboard.html
        ├── task_list.html
        ├── task_detail.html
        ├── task_form.html
        ├── project_list.html
        ├── project_detail.html
        └── project_form.html
```


## Usage
1. Access the admin interface at /admin to manage users and roles
2. Regular users can access the dashboard at the root URL /
3. Create projects and assign tasks to team members
4. Track project progress and task completion rates
5. Filter tasks by status and priority

## Contributing

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Create a Pull Request

