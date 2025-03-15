import os
import tempfile
import shutil
import tarfile
import zipfile
import git
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .serializers import AnalysisRequestSerializer
from staticAnalysis.semgrep_analysis import run_semgrep_analysis

class CodeAnalysisView(APIView):
    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {'type': 'string', 'format': 'binary'},
                    'source_code': {'type': 'string'},
                    'lang': {'type': 'string'},
                    'repo_url': {'type': 'string', 'format': 'uri'},
                },
                'example': {
                    'file': '(binary file data)',
                    'description': 'A sample file upload'
                }
            }
        },
        responses={200: {'type': 'string', 'example': 'File uploaded successfully'}}
    )
    def post(self, request, *args, **kwargs):
        serializer = AnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            temp_dir = tempfile.mkdtemp()
            try:
                if 'file' in data:
                    file = data['file']
                    if file.name.endswith('.zip'):
                        with zipfile.ZipFile(file, 'r') as zip_ref:
                            zip_ref.extractall(temp_dir)
                    elif file.name.endswith('.tar.gz'):
                        with tarfile.open(fileobj=file, mode='r:gz') as tar_ref:
                            tar_ref.extractall(temp_dir)
                    else:
                        return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'source_code' in data:
                    source_code = data['source_code']
                    lang = data.get('lang')
                    if not lang:
                        return Response({'error': 'Language must be specified for source code snippets.'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    lang_extensions = {
                        'python': 'py',
                        'javascript': 'js',
                        'java': 'java',
                        'c': 'c',
                        'cpp': 'cpp',
                        'ruby': 'rb',
                        'go': 'go',
                        'php': 'php',
                        'swift': 'swift',
                        'typescript': 'ts',
                        'kotlin': 'kt',
                        'scala': 'scala',
                        'rust': 'rs',
                        'perl': 'pl',
                        'r': 'r',
                        'shell': 'sh',
                        'html': 'html',
                        'css': 'css',
                    }

                    if lang not in lang_extensions:
                        return Response({'error': f'Unsupported language: {lang}'}, status=status.HTTP_400_BAD_REQUEST)

                    file_extension = lang_extensions[lang]
                    temp_file_path = os.path.join(temp_dir, f'source_code.{file_extension}')
                    with open(temp_file_path, 'w') as temp_file:
                        temp_file.write(source_code)
                elif 'repo_url' in data:
                    repo_url = data['repo_url']
                    git.Repo.clone_from(repo_url, temp_dir)
                else:
                    return Response({'error': 'No valid input provided'}, status=status.HTTP_400_BAD_REQUEST)

                analysis_results = run_semgrep_analysis(temp_dir)
                return Response(analysis_results, status=status.HTTP_200_OK)
            finally:
                shutil.rmtree(temp_dir)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)