from django.urls import path
from .views import WorksList

app_name = 'todolist'

urlpatterns = [
    path('list/', WorksList.as_view(), name='list'),
]