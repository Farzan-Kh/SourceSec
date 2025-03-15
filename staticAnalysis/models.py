import uuid
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class RepoProject(Project):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()

    def __str__(self):
        return f"RepoProject {self.name}"

class CodeProject(Project):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()

    def __str__(self):
        return f"CodeProject {self.name}"

class Snapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assessment_result = models.JSONField()

    class Meta:
        abstract = True

class ProjectSnapshot(Snapshot):
    project = models.ForeignKey(CodeProject, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_snapshots/')

    def __str__(self):
        return f"ProjectSnapshot {self.id} for project {self.project.name}"

class RepoSnapshot(Snapshot):
    project = models.ForeignKey(RepoProject, on_delete=models.CASCADE)
    repo_url = models.URLField()

    def __str__(self):
        return f"RepoSnapshot {self.id} for project {self.project.name}"
