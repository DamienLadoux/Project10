from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects_created",
    )

class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_contributions",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    permission = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issues_created",
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issues_assigned",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    
class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
