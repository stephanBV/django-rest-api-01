from django.shortcuts import render
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from todos.serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from todos.models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from todos.pagination import CustomPageNumberPagination

# Create your views here.
class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] #django_filters provide different ways to filter the data 
    filterset_fields = ['id', 'title', 'is_complete'] #we can now filter data by id, title or is_complete, e.g. ../api/todos/?id=3
    search_fields = ['id', 'title', 'desc', 'is_complete'] #i can now look for a specific word for e.g. in id, title, desc or is_complete
    ordering_fields = ['id', 'title', 'desc', 'is_complete']

    def perform_create(self, serializer): #GET
        return serializer.save(owner=self.request.user)

    #only retrieve items created by the current user
    def get_queryset(self): #POST
        return Todo.objects.filter(owner=self.request.user)

class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=TodoSerializer
    permission_classes=(IsAuthenticated,)
    lookup_field = "id"

    #do anything only if the owner is person logged in
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)