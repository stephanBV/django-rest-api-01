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

when creating a django model we need some info:

- when objects of that model are created
- when they are updated
- how they are retrieved
  --> things that are common to all models of the application (but not provided by django out-of-the-box)
  --> we created a helpers folder and add a model

Abstract base classes are useful when you want to put some common information into a number of other models. You write your base class and put abstract=True in the Meta class. This model will then not be used to create any database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child class.
https://docs.djangoproject.com/en/3.2/topics/db/models/
