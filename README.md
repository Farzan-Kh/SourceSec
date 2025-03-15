# My Django Static Analysis App

This is a Django web application that accepts source code from users, performs static analysis using Semgrep, and returns the analysis results.

## Features

- Accepts user-submitted source code.
- Performs static analysis using Semgrep.
- Displays analysis results to users.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-django-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the development server:
   ```
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`.

3. Submit your source code for analysis through the provided interface.

## Requirements

- Python 3.x
- Django
- Semgrep

## License

This project is licensed under the MIT License.