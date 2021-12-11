from django.urls import path
from .views import WorksList, FilterView, GetChildren, index

app_name = 'todolist'

urlpatterns = [
    path('', index, name='index'),
    path('list/', WorksList.as_view(), name='list'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('list/children/<int:pk>/', GetChildren.as_view(), name='get_children')
]