from rest_framework import status

from .test_setup import TestSetUp


class TestAuthentication(TestSetUp):

    def register_user(self):
        register_request_body = {
            'email': self.user_data['email'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password'],
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
        }
        return self.client.post(self.register_url, register_request_body)

    def login_user(self, login_request_body):
        if not login_request_body:
            login_request_body = {
                'email': self.user_data['email'],
                'password': self.user_data['password']
            }
        return self.client.post(self.login_url, login_request_body)

    def test_user_register_success(self):
        res = self.register_user()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_register_fail_no_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Todo: Add a test for checking email verification after implementing it

    def test_user_login_success(self):
        self.register_user()
        res = self.login_user()
        # Todo: Add forced email verification here
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_failure_invalid_credentials(self):
        self.register_user()
        res = self.login_user()
