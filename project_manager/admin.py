from django.contrib import admin
from .models import Project, Document, Task, Milestone

admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Document)
admin.site.register(Task)