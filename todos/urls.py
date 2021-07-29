from todos.views import TodosAPIView
from django.urls import path

urlpatterns = [
    path("", TodosAPIView.as_view(), name="todos")
    ]