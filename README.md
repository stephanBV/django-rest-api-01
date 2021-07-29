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

#### end set up

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
- also added a token method to generate a token for the user, we add @property to treat the token as a property so we can just do user.token without having to instantiate a class.

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

#### end unit testing

#### User registration

RegisterSerializer -> RegisterAPIView -> path in urls

### end user registration

### Authenticate user

pip install pyjwt
LoginSerializer -> LoginAPIView -> token method in class User in models -> path in urls

#### end authenticate user

### JWT API Authentication

- views.py -> AuthUserAPIView
- urls -> path user
  -- TypeError: 'BasePermissionMetaclass' object is not iterable
  --> a missing comma ',' at the end of permission_classes = (permissions.IsAuthenticated)
  in autentication/views.py/AuthUserAPIView
  --> should be (permissions.IsAuthenticated,)
  -- "detail": "Authentication credentials were not provided."
  --> missing Authorization: Bearer <token>: The bearer token is generated by the server in response to a login request.
  ---> need to setup jwt authentication for the application
- created jwt.py -> class JWTAuthentication
- settings.py: <!-- https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication -->
  -- INSTALLED_APP = ['authentication']
  -- REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
  'authentication.jwt.JWTAuthentication',
  ]
  }
- The above will apply JWT authentication on all views, but some views like register or login don't require a token so add authentication_classes = [] for views that don't require jwt auth

### end JWT API Authentication
#### List and Create APIViews 
COMMON for CREATE and LIST:
- todos/ models -> Todo (inh from helpers (TrackingModel))
- todos/ serializers -> TodoSerializer (inh from ModelSerializer)
- python manage.py makemigrations
- python manage.py migrates
Notes: on_delete=models.CASCADE -> delete everything from the owner
CREATE:
- todos/ views -> CreateTodoAPIView (inh from CreateAPIView, overr perform_create)
- todos/ urls -> 'create'

LIST:
- todos/ views -> TodoListAPIView (inh from ListAPIView, overr get_queryset)
- todos/ urls -> 'list'
### end List and Create APIViews 01 ###
#### ListCreateAPIView to create AND list items
we can use one view to both create and list the items:
- replace CreateTodoAPIView and TodoListAPIView by TodosAPIView inheriting from ListCreateAPIView
- change url
### end ListCreateAPIView to create AND list items ###
### Retrieve Update and Destroy APIViews
Django has a built-in class that can update, retrieve and delete items: RetrieveUpdateDestroyAPIView
- add TodoDetailAPIView inheriting from RetrieveUpdateDestroyAPIView
- add path("<int:id>", TodoDetailAPIView.as_view(), name="todo") to urls
### end Retrieve Update and Destroy APIViews ###
#### Filtering, Searching, and Ordering
- pip install django_filter
- add django_filters to INSTALLED_APPS
- in views.py:
- django_filters provide different ways to filter the data 
-- Filter: we can now filter data by id, title or is_complete, e.g. ../api/todos/?id=3
- Search: also, from rest_framework import filters -> filters.SearchFilter -> can now look for specific word for e.g.
- Order: filters.OrderingFilter --> /?ordering=id
### end Filtering, Searching, and Ordering ###
### API Pagination
To limit the nmber fo results sent back to us we can use django pagination methods
- LimitOffsetPagination:
-- settings -> REST_FRAMEWORK -> 'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.LimitOffsetPagination"
-- e.g. ../api/todos/?limit=1
-- e.g. ..api/todos/?limit=4&offset=20 -> ignore the first 20 items and retrieve the next 4
- PageNumberPagination:
-- settings -> DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.PageNumberPagination", 'PAGE_SIZE':5
-- will return 5 items per page
-- to avoid having to add the number of items per page in settings, we can create a custom pagination
- Custom Pagination:
-- create pagination.py
-- CustomPageNumberPagination inherit from pagination.PageNumberPagination
-- views -> TodosAPIView -> pagination_class = CustomPageNumberPagination
-- now by default api/todos/ will automatically retrieve what is in pagination.py
### end API Pagination