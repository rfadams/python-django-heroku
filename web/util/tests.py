from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from factories import *


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.loggedin_client = Client()
        self.user = UserFactory()
        self.loggedin_client.login(username='john@example.com', password='secret')

    def test_user_creation_authentication(self):
        """
        Test that a user was created in the database and is real
        """
        c = self.loggedin_client

        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

        session = c.session
        session['somekey'] = 'test'
        session.save()
        self.assertIn('somekey', session.keys()) 
        self.assertIn('test', session.values())



