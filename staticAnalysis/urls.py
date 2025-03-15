from django.urls import path
from django.contrib.auth import views as auth_views
from .views import analyze_code, user_projects, add_project, delete_project, project_detail, add_project_snapshot, add_repo_snapshot, signup

urlpatterns = [
    path('', analyze_code, name='analyze_code'),
    path('projects/', user_projects, name='user_projects'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/delete/<uuid:project_id>/', delete_project, name='delete_project'),
    path('projects/<uuid:project_id>/', project_detail, name='project_detail'),
    path('projects/<uuid:project_id>/add_project_snapshot/', add_project_snapshot, name='add_project_snapshot'),
    path('projects/<uuid:project_id>/add_repo_snapshot/', add_repo_snapshot, name='add_repo_snapshot'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', signup, name='signup'),
]