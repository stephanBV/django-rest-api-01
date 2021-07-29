from rest_framework.test import APITestCase
from django.urls import reverse #reverse allows to access an endpoint by its name
from rest_framework import status
from todos.models import Todo

# Create your tests here.
class Todos_APITestCase(APITestCase):
    def create_todo(self):
        sample_todo= {'title':'hello', "desc":'Test'}
        response = self.client.post(reverse("todos"), sample_todo)
        return response

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


class TestListCreateTodos(Todos_APITestCase):
    #when we inherit from APITestCase, we get access to a client (similar to Postman for e.g.)
    #which means we have now access to all capabilities of a client (get, post, etc..)
    def test_should_not_creates_todo_with_no_auth(self):
        sample_todo= {'title':'hello', "desc":'Test'}
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo(self):
        #capture the current size of the database of todos
        previous_todo_count = Todo.objects.all().count()
        #authenticate
        self.authenticate()
        #create data
        sample_todo= {'title':'hello', "desc":'Test'}
        #request post todo item
        response = self.create_todo()
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
        self.create_todo()

        res = self.client.get(reverse("todos"))
        #check type of count
        self.assertIsInstance(res.data['count'], int) #count is part of the metadata in the response
        #check the actual count after one item added
        self.assertEqual(res.data['count'], 1)

class Test_TodoDetailAPIView(Todos_APITestCase):

    def test_retrieves_one_item(self):
        self.authenticate()
        response = self.create_todo()

        #post todo with a dynamic id
        res = self.client.get(reverse("todo", kwargs={'id': response.data['id']}))
        #check it passes
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #check it has been saved in the db
        todo=Todo.objects.get(id=response.data['id'])
        #check that what is in the db matches with what we posted
        self.assertEqual(todo.title, res.data['title'])

    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_todo()

        #update created todo item
        res=self.client.patch(
            reverse("todo", kwargs={'id': response.data['id']}), 
            {"title":"new test title", 'is_complete':True}
            )
        #check it passes
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_todo = Todo.objects.get(id=response.data['id'])
        #check is_complete is true
        self.assertEqual(updated_todo.is_complete, True)
        #check new title
        self.assertEqual(updated_todo.title, "new test title")

    def test_deletes_one_item(self):
        self.authenticate()
        response = self.create_todo()

        # res = self.client.delete(reverse("todo", kwargs={'id':response.data['id']}), {})
        # self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # deleted_todo = len(Todo.objects.all())
        # self.assertEqual(deleted_todo, 0)

        #get number of items in db (1)
        prev_db_count=Todo.objects.all().count()
        #check it's greater than 0
        self.assertGreater(prev_db_count, 0)
        #check it's equal to 1
        self.assertEqual(prev_db_count, 1)

        #make delete request
        response = self.client.delete(reverse("todo", kwargs={'id':response.data['id']}))
        #check status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #check db has reduced
        self.assertEqual(Todo.objects.all().count(), 0)