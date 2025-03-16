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
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': "Upload a file for analysis. Mutually exclusive with `repo_url` and `source_code` + `lang`.",
                    },
                    'repo_url': {
                        'type': 'string',
                        'format': 'uri',
                        'description': "Provide a repository URL for analysis. Mutually exclusive with `file` and `source_code` + `lang`.",
                    },
                    'source_code': {
                        'type': 'string',
                        'description': "Provide raw source code for analysis. Must be used with `lang`. Mutually exclusive with `file` and `repo_url`.",
                    },
                    'lang': {
                        'type': 'string',
                        'description': "Specify the programming language of the source code. Must be used with `source_code`.",
                    },
                },
                'required': [],
            }
        },
        responses={
            200: {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'check_id': {'type': 'string'},
                        'location_path': {'type': 'string'},
                        'location_start_line': {'type': 'integer'},
                        'location_start_col': {'type': 'integer'},
                        'message': {'type': 'string'},
                        'metadata_category': {'type': 'string'},
                        'metadata_impact': {'type': 'string'},
                    },
                },
            },
            400: {'description': 'Bad Request'},
        },
        examples=[
            OpenApiExample(
                'File Upload Example',
                value={'file': '(binary file data)'},
                request_only=True,
            ),
            OpenApiExample(
                'Repository URL Example',
                value={'repo_url': 'https://github.com/example/repo.git'},
                request_only=True,
            ),
            OpenApiExample(
                'Source Code Example',
                value={'source_code': 'print("Hello, World!")', 'lang': 'python'},
                request_only=True,
            ),
        ],
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
                elif 'source_code' in data and 'lang' in data:
                    source_code = data['source_code']
                    lang = data['lang']
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
                    return Response(
                        {"error": "Invalid input parameters."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Run Semgrep analysis
                results = run_semgrep_analysis(temp_dir)
                return Response(results, status=status.HTTP_200_OK)
            finally:
                shutil.rmtree(temp_dir)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)