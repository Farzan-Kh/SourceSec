# Django Static Analysis App

This is a Django-based web application that allows users to upload source code, project files, or repository URLs for static analysis. The application uses **Semgrep** to perform the analysis and provides detailed results, including vulnerabilities, metadata, and impact.


## Features

- **User Authentication**: Users can sign up, log in, and manage their projects.
- **Static Code Analysis**: Analyze code snippets, project files, or repositories using Semgrep.
- **Project Management**: Create, view, and delete projects.
- **Snapshot Management**: Add snapshots for projects or repositories and view their analysis results.
- **Severity Visualization**: Visualize the severity of vulnerabilities using progress indicators.
- **REST API**: Expose an API endpoint for programmatic access to the analysis functionality.
- **Swagger Documentation**: Auto-generated API documentation using DRF Spectacular.


## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Documentation](#api-documentation)
4. [Project Structure](#project-structure)
5. [Key Features](#key-features)
6. [Requirements](#requirements)
7. [Contributing](#contributing)
8. [License](#license)


## Installation

### Prerequisites

- Python 3.8 or higher
- Django 5.1.7
- Semgrep installed on your system (`pip install semgrep` or [Semgrep Installation Guide](https://semgrep.dev/docs/installation/))

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Farzan-Kh/SourceSec.git
   cd my-django-app
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a .env file in the root directory and add the following:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.


## Usage

### Web Interface

1. **Sign Up**: Create an account using the sign-up page.
2. **Log In**: Log in to access the dashboard.
3. **Add Projects**: Create a new project (repository or code-based).
4. **Upload Snapshots**: Add snapshots for projects or repositories.
5. **View Results**: Analyze vulnerabilities and metadata in the results page.

### REST API

The application provides a REST API for programmatic access to the analysis functionality.

- **Endpoint**: `/api/analyze/`
- **Methods**: `POST`
- **Parameters**:
  - `file`: Upload a `.zip` or `.tar.gz` file.
  - `source_code`: Provide raw source code as a string.
  - `repo_url`: Provide a repository URL.
  - `lang`: Specify the language for source code snippets (e.g., `python`, `javascript`).

Example cURL request:
```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -F "source_code=print('Hello, World!')" \
  -F "lang=python"
```


## API Documentation

The API is documented using Swagger and can be accessed at:

- **Swagger UI**: [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)
- **Schema Endpoint**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)


## Project Structure

```
.
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── .vscode/                    # VS Code configuration
├── db.sqlite3                  # SQLite database
├── django_root/                # Django project root
│   ├── __init__.py             # Blank init file
│   ├── asgi.py                 # ASGI configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Project-level URL routing
│   ├── wsgi.py                 # WSGI configuration
├── manage.py                   # Django management script
├── project_snapshots/          # Uploaded project snapshots
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── rest_api/                   # REST API app
│   ├── __init__.py             # Blank init file
│   ├── serializers.py          # API serializers
│   ├── urls.py                 # API URL routing
│   ├── views.py                # API views
├── staticAnalysis/             # Main app for static analysis
│   ├── __init__.py             # Blank init file
│   ├── admin.py                # Admin configuration
│   ├── apps.py                 # App configuration
│   ├── migrations/             # Database migrations
│   ├── models.py               # Database models
│   ├── semgrep_analysis.py     # Semgrep integration logic
│   ├── templates/              # HTML templates
│   ├── templatetags/           # Custom Django template filters
│   ├── tests.py                # Unit tests
│   ├── urls.py                 # App-level URL routing
│   ├── views.py                # View logic
```


## Key Features

### 1. **Static Analysis**
- Uses Semgrep to analyze code for vulnerabilities.
- Supports multiple input types: code snippets, project files, and repositories.

### 2. **User Projects**
- Manage projects with detailed descriptions.
- Add snapshots for code or repositories.

### 3. **Snapshot Analysis**
- View detailed results for each snapshot, including:
  - Vulnerability category
  - Impact
  - CWE (Common Weakness Enumeration)
  - OWASP (Open Web Application Security Project) references

### 4. **Custom Filters**
- Includes a custom Django template filter (`skip_parents`) for truncating file paths in analysis results.

### 5. **REST API**
- Exposes an API endpoint for external integrations.
- Fully documented with Swagger.


## Requirements

- **Python**: 3.8 or higher
- **Django**: 5.1.7
- **Semgrep**: Installed on the system
- **Other Dependencies**: Listed in requirements.txt


## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
