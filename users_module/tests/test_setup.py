from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):


    def setUp(self):
        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')

        self.user_data = {
            'email': 'email@gmail.com',
            'password': 'password1234',
            'first_name': 'test',
            'last_name': 'user'
        }

        return super(TestSetUp, self).setUp()

    def tearDown(self):

        return super(TestSetUp, self).tearDown()