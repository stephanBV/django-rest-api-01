from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from todos.serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from todos.models import Todo
# Create your views here.
class CreateTodoAPIView(CreateAPIView):
    #note: inherited CreateAPIView handles the POST request for us
    serializer_class = TodoSerializer
    #the user needs to be autenticated to create a todo item
    permission_classes = (IsAuthenticated, )

    #set the owner of the created todo items as the person currently logged in
    #override performe_create
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

class TodoListAPIView(ListAPIView):
    serializer_class=TodoSerializer
    permission_classes=(IsAuthenticated,)

    #override get_query_set from ListAPIView to return todo itms from the current person logged in
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)