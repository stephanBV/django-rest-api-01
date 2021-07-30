#### Django Rest API for a todo app with JWT auth, unittested, deployed on heroku and documented with swagger

#### Set up ###
Git clone this repo.  
Then:
```
mkdir django-rest-api-01
cd django-rest-api-todo-app
virtualenv venv
source venv/bin/activate (on bash, not working with zsh)
pip install requirements.txt
python manage.py runserver
```
You can use Thunder Client on vscode or Postman to make requests. <br />
Live deploy swagger: https://django-rest-todo-app.herokuapp.com/swagger/ <br />
Live deploy redoc: https://django-rest-todo-app.herokuapp.com/redoc/
