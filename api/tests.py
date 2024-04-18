from django.test import TestCase
from django.test import Client


# Create your tests here.
class TestApiViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response, "api/users/")

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        print(response.json())
