from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from .views import WorksList


class TestingWorkList(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='Matinmat88', password='aliMatinMat89')

    def testing_work_list(self):
        request = self.factory.get('list')
        request.user = self.user
        response = WorksList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.user, self.user)

