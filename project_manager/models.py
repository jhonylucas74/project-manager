from django.db import models

class Status(models.TextChoices):
    BACKLOG = 'backlog', 'Backlog'
    TODO = 'todo', 'To Do'
    DOING = 'doing', 'Doing'
    DONE = 'done', 'Done'
    BLOCKED = 'blocked', 'Blocked'
    ARCHIVED = 'archived', 'Archived'

class Document(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BACKLOG)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    documents = models.ManyToManyField('Document', related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MilestoneStatus(models.TextChoices):
    NOT_STARTED = 'not_started', 'Not Started'
    IN_PROGRESS = 'in_progress', 'In Progress'
    DELAYED = 'delayed', 'Delayed'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    BLOCKED = 'blocked', 'Blocked'

class Milestone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='milestones')
    status = models.CharField(max_length=15, choices=MilestoneStatus.choices, default=MilestoneStatus.NOT_STARTED)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    milestone = models.ForeignKey('Milestone', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    owner = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BACKLOG)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
