import os
import tempfile
import shutil
import tarfile
import zipfile
import git
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectSnapshot, RepoSnapshot, RepoProject, CodeProject
from itertools import chain
from .semgrep_analysis import run_semgrep_analysis
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

@login_required
def user_projects(request):
    projects = list(chain(RepoProject.objects.filter(user=request.user), CodeProject.objects.filter(user=request.user)))

    for project in projects:
        if isinstance(project, RepoProject):
            latest_snapshot = RepoSnapshot.objects.filter(project=project).order_by('-created_at').first()
        elif isinstance(project, CodeProject):
            latest_snapshot = ProjectSnapshot.objects.filter(project=project).order_by('-created_at').first()
        else:
            latest_snapshot = None
        
        if latest_snapshot:
            severity_mapping = {
                'HIGH': 3,
                'MEDIUM': 2,
                'LOW': 1,
                'none': 0
            }

            max_severity = max(
                (result['metadata_impact'] for result in latest_snapshot.assessment_result),
                key=lambda severity: severity_mapping.get(severity, 0),
                default='none'
            )
            project.max_severity = max_severity
        else:
            project.max_severity = 'none'

    return render(request, 'static_analysis/user_projects.html', {'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        project_type = request.POST.get('project_type')
        if name and project_type:
            if project_type == 'repo':
                RepoProject.objects.create(id=uuid.uuid4(), user=request.user, name=name, description=description)
            elif project_type == 'code':
                CodeProject.objects.create(id=uuid.uuid4(), user=request.user, name=name, description=description)
            return redirect('user_projects')
    return render(request, 'static_analysis/add_project.html')

@login_required
def delete_project(request, project_id):
    if RepoProject.objects.filter(id=project_id, user=request.user).exists():
        project = RepoProject.objects.get(id=project_id, user=request.user)
    elif CodeProject.objects.filter(id=project_id, user=request.user).exists():
        project = CodeProject.objects.get(id=project_id, user=request.user)
    else:
        return render(request, '404.html', status=404)
    if project:
        project.delete()
    return redirect('user_projects')

@login_required
def project_detail(request, project_id):
    # project = get_object_or_404(RepoProject.objects.filter(id=project_id, user=request.user) | CodeProject.objects.filter(id=project_id, user=request.user))
    if RepoProject.objects.filter(id=project_id, user=request.user).exists():
        project = RepoProject.objects.get(id=project_id, user=request.user)
    elif CodeProject.objects.filter(id=project_id, user=request.user).exists():
        project = CodeProject.objects.get(id=project_id, user=request.user)
    else:
        return render(request, '404.html', status=404)
    if isinstance(project, CodeProject):
        snapshots = ProjectSnapshot.objects.filter(project=project).order_by('-id')
        snapshot_url = 'add_project_snapshot'
    elif isinstance(project, RepoProject):
        snapshots = RepoSnapshot.objects.filter(project=project).order_by('-id')
        snapshot_url = 'add_repo_snapshot'
    else:
        snapshots = []
        snapshot_url = None
    return render(request, 'static_analysis/project_detail.html', {'project': project, 'snapshots': snapshots, 'snapshot_url': snapshot_url})

@login_required
def add_project_snapshot(request, project_id):
    project = CodeProject.objects.get(id=project_id, user=request.user)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            temp_dir = tempfile.mkdtemp()
            try:
                # Extract the file to the temporary directory
                if file.name.endswith('.zip'):
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif file.name.endswith('.tar.gz'):
                    with tarfile.open(fileobj=file, mode='r:gz') as tar_ref:
                        tar_ref.extractall(temp_dir)
                else:
                    return JsonResponse({'error': 'Unsupported file format'}, status=400)

                # Run semgrep on the extracted directory
                analysis_results = run_semgrep_analysis(temp_dir)

                # Save the snapshot
                ProjectSnapshot.objects.create(project=project, file=file, assessment_result=analysis_results)
            finally:
                # Remove the temporary directory
                shutil.rmtree(temp_dir)
            return redirect('project_detail', project_id=project.id)
    return render(request, 'static_analysis/add_project_snapshot.html', {'project': project})

@login_required
def add_repo_snapshot(request, project_id):
    project = RepoProject.objects.get(id=project_id, user=request.user)
    if request.method == 'POST':
        repo_url = request.POST.get('repo_url')
        if repo_url:
            temp_dir = tempfile.mkdtemp()
            try:
                # Clone the repository to the temporary directory
                git.Repo.clone_from(repo_url, temp_dir)
                analysis_results = run_semgrep_analysis(temp_dir)

                # Save the snapshot
                RepoSnapshot.objects.create(project=project, repo_url=repo_url, assessment_result=analysis_results)
            finally:
                # Remove the temporary directory
                shutil.rmtree(temp_dir)
            return redirect('project_detail', project_id=project.id)
    return render(request, 'static_analysis/add_repo_snapshot.html', {'project': project})

def analyze_code(request):
    if request.method == 'POST':
        if 'source_code' in request.POST:
            source_code = request.POST.get('source_code')
            language = request.POST.get('language')
            if source_code and language:
                temp_dir = tempfile.mkdtemp()
                try:
                    extension = {
                        'python': 'py',
                        'javascript': 'js',
                        'java': 'java',
                        'csharp': 'cs',
                        'cpp': 'cpp',
                        'ruby': 'rb',
                        'php': 'php',
                        'go': 'go',
                        'swift': 'swift'
                    }.get(language, 'txt')
                    temp_file_path = os.path.join(temp_dir, f'source_code.{extension}')
                    with open(temp_file_path, 'w') as temp_file:
                        temp_file.write(source_code)
                    analysis_results = run_semgrep_analysis(temp_dir)
                finally:
                    shutil.rmtree(temp_dir)
                return render(request, 'static_analysis/analyze_code.html', {'results': analysis_results})
        elif 'file' in request.FILES:
            file = request.FILES.get('file')
            if file:
                temp_dir = tempfile.mkdtemp()
                try:
                    # Extract the file to the temporary directory
                    if file.name.endswith('.zip'):
                        with zipfile.ZipFile(file, 'r') as zip_ref:
                            zip_ref.extractall(temp_dir)
                    elif file.name.endswith('.tar.gz'):
                        with tarfile.open(fileobj=file, mode='r:gz') as tar_ref:
                            tar_ref.extractall(temp_dir)
                    else:
                        return JsonResponse({'error': 'Unsupported file format'}, status=400)

                    # Run semgrep on the extracted directory
                    analysis_results = run_semgrep_analysis(temp_dir)
                finally:
                    # Remove the temporary directory
                    shutil.rmtree(temp_dir)
                return render(request, 'static_analysis/analyze_code.html', {'results': analysis_results})
        elif 'repo_url' in request.POST:
            repo_url = request.POST.get('repo_url')
            if repo_url:
                temp_dir = tempfile.mkdtemp()
                try:
                    # Clone the repository to the temporary directory
                    git.Repo.clone_from(repo_url, temp_dir)
                    analysis_results = run_semgrep_analysis(temp_dir)
                finally:
                    # Remove the temporary directory
                    shutil.rmtree(temp_dir)
                return render(request, 'static_analysis/analyze_code.html', {'results': analysis_results})
        else:
            return JsonResponse({'error': 'No source code, file, or repo URL provided'}, status=400)
    return render(request, 'static_analysis/analyze_code.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user_projects')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def index(request):
    return render(request, 'static_analysis/index.html')