from django.contrib import admin
from .models import RepoProject, CodeProject, ProjectSnapshot, RepoSnapshot

admin.site.register(RepoProject)
admin.site.register(CodeProject)
admin.site.register(ProjectSnapshot)
admin.site.register(RepoSnapshot)
