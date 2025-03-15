from django.urls import path
from .views import CodeAnalysisView

urlpatterns = [
    path('analyze/', CodeAnalysisView.as_view(), name='code_analysis'),
]