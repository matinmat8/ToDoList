from django.urls import path
from .views import WorksList, FilterView

app_name = 'todolist'

urlpatterns = [
    path('list/', WorksList.as_view(), name='list'),
    path('filter/', FilterView.as_view(), name='filter')
]