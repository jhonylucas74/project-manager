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
