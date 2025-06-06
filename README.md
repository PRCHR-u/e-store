#e-store
This project is a work-in-progress online store built with Django. It is being developed as part of a course.

## Technologies Used

* Python
* Django

## Setup

1. Clone the repository.
2. Navigate to the project directory.
3. Create and activate a virtual environment:


bash python -m venv venv source venv/bin/activate # On macOS/Linux venv\Scripts\activate # On Windows

4. Install dependencies:


bash pip install -r requirements.txt # You'll create this later

5. Run migrations:


bash python manage.py migrate

6. Run the development server:


bash python manage.py runserver

## GitFlow

This project uses GitFlow. The main branches are `main` and `develop`