#drf-todolist-app

#### Set up

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
  ### end set up

#### Customize model for authentication

authentication/model.py:

- Because we are adding a new User model for authentication while dango already has something similar,
  to avoid the clash add AUTH_USER_MODEL="authentication.User" to settings.py

- Note: Abstract base classes are useful when you want to put some common information into a number of other models. You write your base class and put abstract=True in the Meta class. This model will then not be used to create any database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child class.
  https://docs.djangoproject.com/en/3.2/topics/db/models/

- We want to inherint from base django classes but overriding some methods
  -- Our class User inherits from AbstractUser but we want to override some variables and how objects are created.
  --- UserManager() --> custom manager (class) that specifies how objects are created or retrieved (e.g. soft delete implementation).
  --- In our case , we want to alter the way thongs are created in a way that whenever we create a user, they must specify their email for login/username.
  --- Replaced UserManager with custom MyUserManager, in class User
  --- Created class MyUserManager, inheriting from UserManager
  -- Our class MyuserManager inherits from UserManager but we override create_user and create_superuser
- User, added email_verified copied from is_active variable, with the default to false
- also added a token method to generate a token for the user, we add @property to treat the token as a property so we can just do user.token without having to instatntiate a class.

Notes: error -> ValueError: Dependency on app with no migrations: authentication; because we need to propagate changes you make to our models into our database schema.
--> python manage.py makemigrations
-- Then in authentication/migrations/0001_initial.py, we can see that django has created the model User.
--> python manage.py migrate
#### end Customize model for authentication ####

#### Unit Testing

installed live server extension
pip install coverage
added .coveragerc to to define what we want and don't want to cover
coverage run manage.py test && coverage report && coverage htm
--> it created .coverage and htmlcov
we see that authentication/models.py is not at 100%
in htmlcov/ find index.html and click Go Live on vscode bottom right button
--> once opened, click on authentication/models.py; where it's red it means it needs tests
deleted test.py in authentication/
created tests/ folder, \_init_py and test*models.py
Important note: when creating a test, always start with 'test*'.
