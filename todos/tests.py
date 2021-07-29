from rest_framework.test import APITestCase
from django.urls import reverse #reverse allows to access an endpoint by its name
from rest_framework import status
from todos.models import Todo

# Create your tests here.
class TestListCreateTodos(APITestCase):

    def authenticate(self):
        #simulate registration
        self.client.post(reverse("register"), 
        {"username":"username", 
        "email":"email@gmail.com", 
        "password":"testpassword"})
        #simulate login and pass value sent back to us to variable 'response'
        response = self.client.post(reverse("login"), {"email":"email@gmail.com", "password":"testpassword"})
        #add the header to the client: make the credentials equal to Bearer <token>
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    #when we inherit from APITestCase, we get access to a client (similar to Postman for e.g.)
    #which means we have now access to all capabilities of a client (get, post, etc..)
    def test_should_not_creates_todo_with_no_auth(self):
        sample_todo= {'title':'hello', "desc":'Test'}
        response = self.client.post(reverse("todos"), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo(self):
        #capture the current size of the database of todos
        previous_todo_count = Todo.objects.all().count()
        #authenticate
        self.authenticate()
        #create data
        sample_todo= {'title':'hello', "desc":'Test'}
        #request post todo item
        response = self.client.post(reverse("todos"), sample_todo)
        #check if the database has increased by 1 item
        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        #check item has been been created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #check that the title returned is good
        self.assertEqual(response.data['title'], 'hello')
        #check that the description returned is good
        self.assertEqual(response.data['desc'],'Test')

    def test_retrieve_all_todos(self):
        #check GET todos
        self.authenticate()
        response = self.client.get(reverse("todos"))
        #check it passes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #check we have the results
        self.assertIsInstance(response.data['results'], list)

        ### check pagination ###
        sample_todo= {'title':'hello', "desc":'Test'}
        self.client.post(reverse("todos"), sample_todo)

        res = self.client.get(reverse("todos"))
        #check type of count
        self.assertIsInstance(res.data['count'], int) #count is part of the metadata in the response
        #check the actual count after one item added
        self.assertEqual(res.data['count'], 1)