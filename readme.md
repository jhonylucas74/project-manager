# Project Manager

## Description

Project Manager is a Django-based web application designed as a challenge for 'Base dos Dados'.

## Features
- Create new projects with details such as name, description, start date, and end date.
- Upload documents to any project.
- Create milestones and associate them with projects, including status and dates for control.
- Assign tasks to projects and milestones, providing information such as task name, description, status, and assigned user.
- Manage users with different levels of access and permissions.

## Prerequisites
- Docker
- Python
- Pyenv

## Installation

Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
```

On Windows:
```bash
venv\Scripts\activate
```

On Windows with gitbash:
```bash
source ./venv/Scripts/activate
```

On macOS and Linux:
```bash
source venv/bin/activate
```

After activating the virtual environment, install all the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. Create a new `.env` file in the project root directory.

2. Refer to env.example to see which environment variables you need to create. In the example, we have the default values to run following this readme.

## Database Setup

1. Run Docker Compose to start the database: 
  
```bash
docker-compose up -d
```

2. Perform database migrations:

```bash
python3 manage.py migrate
```

3. Run the command to populate the group permissions:

```bash
python3 manage.py populate_permissions
```

4. Create a superuser for the application: 

```bash
python3 manage.py createsuperuser
```

## Running the Server

1. Start the development server:

```bash
python3 manage.py runserver 
```

2. Test your setup by visiting the admin page and logging in:

- http://localhost:8000/admin/

## API Documentation

This project is using Swagger, so to check all the APIs, just access the following link:

- http://127.0.0.1:8000/swagger/

## Group Permissions

This project, by default, creates 3 different groups/roles:

- Owner
- Manager
- Member

Every new user is associated with the Member role. To change any user's role, please access the Django admin. Below are more details about the roles' restrictions:

- Owner: Can access, create, edit, and delete everything.
- Manager: Can create everything, as well as edit, but has restrictions on deleting projects.
- Member: Can view everything but is not able to edit, create, or delete.

Everyone can upload documents to the projects.
