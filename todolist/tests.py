from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from .views import WorksList, GetChildren, DeleteWork
from .models import ToDoList


class TestingWorkList(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='Matinmat88', password='aliMatinMat89')

    def testing_work_list(self):
        request = self.factory.get('list')
        request.user = self.user
        response = WorksList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.user, self.user)

    def testing_adding_work(self):
        data = {
            'user': self.user,
            'title': 'this is a test test',
            'due_date': '2022-04-09',
            'description': 'this is a testing test',
            'priority': 'first',
        }

        request = self.factory.post('list', data=data)
        request.user = self.user

        # Skipping the error 'You cannot add messages without installing django.contrib.
        # messages.middleware.MessageMiddleware' through the following code
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = WorksList.as_view()(request)
        self.assertEqual(response.status_code, 302)
        print(dir(response))

    def testing_getting_children(self):
        work_obj = ToDoList.objects.create(
            user=self.user,
            title='this is a test test',
            due_date='2022-04-09',
            description='this is a testing test',
            priority='first',
        )
        request = self.factory.get('list/children/<int:pk>/')
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = GetChildren.as_view()(request, pk=work_obj.pk)
        self.assertEqual(response.status_code, 200)


class TestingDeletingWork(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='Matinmat88', password='aliMatinMat89')
        self.object = ToDoList.objects.create(
            user=self.user,
            pk= 1,
            title='this is a test test',
            due_date='2022-04-09',
            description='this is a testing test',
            priority='first',
        )

    # Testing the confirm page
    def testing_the_getting_of_DeleteView(self):
        request = self.factory.get('/<pk>/delete')
        request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = DeleteWork.as_view()(request, pk=self.object.pk)
        self.assertEqual(response.status_code, 200)
        # print(dir(response))

    # Testing the deleting process
    def testing_the_posting_of_DeleteView(self):
        request = self.factory.post('/<pk>/delete')
        request.user = self.user

        # Skipping the error 'You cannot add messages without installing django.contrib.
        # messages.middleware.MessageMiddleware' through the following code
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = DeleteWork.as_view()(request, pk=self.object.pk)
        self.assertEqual(response.status_code, 302)