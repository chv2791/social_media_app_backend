# social_media_app_backend
Description: Allows users to create or update their profile with a profile picture, bio, and birth date.

#Install required packages: 
Django, djangorestframework, django-rest-knox

#Set up a virtual environment:
python -m venv Project_EF
Project_EF\Scripts\activate.bat

#Run the development server:
cd social_media_app_backend
python manage.py makemigrations app_backend
python manage.py migrate
python manage.py runserver
