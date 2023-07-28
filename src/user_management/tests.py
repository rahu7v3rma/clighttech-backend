import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from django.db import transaction
from rest_framework.test import APIClient

from user_management import views


TEST_USER_EMAIL = 'testmail@test.test'
TEST_USER_WRONG_EMAIL = 'testwrongmail@test.test'
TEST_USER_WRONG_PASSWORD = 'testwrongpassword'
TEST_USER_USERNAME = 'testname'
TEST_USER_PASSWORD = 'testpassword'
TEST_USER_NEW_PASSWORD = 'testnewpassword'


class LoginTestCase(TestCase):
    def tearDown(self):
        get_user_model().objects.get(email=TEST_USER_EMAIL).delete()
        self.user.delete()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
        )
        self.user.save()

    def test_root_url_resolves_to_login(self):
        found = resolve('/user/login')
        self.assertEqual(
            found.func.__name__, views.UserLoginView.as_view().__name__
        )

    def test_login_authentication_with_succesful_login(self):
        client = APIClient()

        response = client.post(
            '/user/login',
            format='json',
            data={
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)

        json_string = response.content.decode(encoding='UTF-8')
        user_data = json.loads(json_string)
        self.assertEqual(user_data['data']['username'], TEST_USER_USERNAME)
        self.assertEqual(user_data['data']['email'], TEST_USER_EMAIL)
        self.assertIn('auth_token', user_data['data'])

    def test_login_authentication_with_failed_login(self):
        client = APIClient()

        response = client.post(
            '/user/login',
            format='json',
            data={'email': TEST_USER_EMAIL, 'password': 'wrongpassword'},
        )

        self.assertEqual(response.status_code, 401)

        json_string = response.content.decode(encoding='UTF-8')
        user_data = json.loads(json_string)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(user_data['message'], 'Bad credentials.')

    def test_logout_authentication_with_success(self):
        client = APIClient()

        response = client.post(
            '/user/login',
            format='json',
            data={
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            },
        )
        user_data = json.loads(response.content.decode(encoding='UTF-8'))

        client = APIClient()
        client.credentials(
            HTTP_X_AUTHORIZATION='Token ' + user_data['data']['auth_token']
        )
        response = client.post('/user/logout')

        self.assertEqual(response.status_code, 200)


class SignUpTestCase(TestCase):
    def tearDown(self):
        self.user.delete()

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='user@test.test',
            username='user@test.test',
            password='user_pass',
        )

    def test_create_new_user(self):
        client = APIClient()
        response = client.post(
            '/user/sign-up',
            format='json',
            data={
                'first_name': 'first_name',
                'last_name': 'last_name',
                'email': 'new_user@test.test',
                'password': 'hzfQvPfG',
            },
        )
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        response_data = json.loads(json_string)
        self.assertEqual(
            response_data['message'], 'User successfully created.'
        )
        user1 = get_user_model().objects.get(email='new_user@test.test')
        self.assertEqual(user1.username, 'new_user@test.test')
        self.assertEqual(user1.first_name, 'first_name')
        self.assertEqual(user1.last_name, 'last_name')

    def test_create_user_with_email_already_exists(self):
        client = APIClient()
        with transaction.atomic():
            response = client.post(
                '/user/sign-up',
                format='json',
                data={
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'email': 'user@test.test',
                    'password': 'hzfQvPfG',
                },
            )
        self.assertEqual(response.status_code, 401)
        json_string = response.content.decode(encoding='UTF-8')
        response_data = json.loads(json_string)
        self.assertEqual(response_data['message'], 'Email already exists.')


class ChangePasswordTestCase(TestCase):
    def tearDown(self):
        get_user_model().objects.get(email=TEST_USER_EMAIL).delete()
        self.user.delete()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
        )
        self.user.save()

    def test_change_password_wrong_password(self):
        client = APIClient()

        response = client.post(
            '/user/login',
            format='json',
            data={
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            },
        )
        user_data = json.loads(response.content.decode(encoding='UTF-8'))
        client.credentials(
            HTTP_X_AUTHORIZATION='Token ' + user_data['data']['auth_token']
        )

        response = client.post(
            '/user/change-password',
            format='json',
            data={
                'new_password': TEST_USER_NEW_PASSWORD,
                'old_password': TEST_USER_WRONG_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 401)
        json_string = response.content.decode(encoding='UTF-8')
        response_data = json.loads(json_string)
        self.assertEqual(response_data['message'], 'Bad credentials.')

    def test_change_password(self):
        # check the user password
        self.assertTrue(self.user.check_password(TEST_USER_PASSWORD))
        client = APIClient()
        response = client.post(
            '/user/login',
            format='json',
            data={
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            },
        )
        user_data = json.loads(response.content.decode(encoding='UTF-8'))
        client.credentials(
            HTTP_X_AUTHORIZATION='Token ' + user_data['data']['auth_token']
        )
        response = client.post(
            '/user/change-password',
            format='json',
            data={
                'new_password': TEST_USER_NEW_PASSWORD,
                'old_password': TEST_USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        response_data = json.loads(json_string)
        self.assertEqual(
            response_data['message'], 'Password changed successfully.'
        )
        # check that the password and the token have been changed
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(TEST_USER_PASSWORD))
        self.assertTrue(self.user.check_password(TEST_USER_NEW_PASSWORD))
        self.assertEqual(
            response_data.get('data').get('new_token'),
            self.user.auth_token.key,
        )
