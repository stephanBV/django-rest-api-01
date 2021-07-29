from todos.views import CreateTodoAPIView, TodoListAPIView
from django.urls import path

urlpatterns = [
    path('create', CreateTodoAPIView.as_view(), name='create-todo'),
    path('list', TodoListAPIView.as_view(), name='list-todos')
    ]