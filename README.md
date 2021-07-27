#drf-todolist-app

virtualenv venv
source venv/bin/activate (on bash, not working with zsh)
pip install django djangorestframework
django-admin startproject todolistapi .
python manage.py runserver
add 'rest_framework' to INSTALLED_APPS to todolistapi/settings.py
python manage.py startapp todos
python manage.py startapp authentication
gitignore.io -> django and paste content to a new .gitgnore file (can also do it directly from github)
