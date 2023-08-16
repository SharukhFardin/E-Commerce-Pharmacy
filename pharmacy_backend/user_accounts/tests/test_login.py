from user_accounts.models import User
from rest_framework.test import APIClient, APITestCase

class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.login_url = '/api/user-login/'

    def test_user_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)

    def test_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)

    def test_missing_fields(self):
        data = {
            'email': 'test@example.com',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

