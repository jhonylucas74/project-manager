from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.me_url = reverse('me')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'Test User'
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_signin(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(self.signin_url, {'email': self.user_data['email'], 'password': self.user_data['password']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_me_authenticated(self):
        user = CustomUser.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(user)
        headers = { 'Authorization': f'Bearer {refresh.access_token}' }
        response = self.client.get(self.me_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)

    def test_get_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_signin_with_wrong_password(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(self.signin_url, {'email': self.user_data['email'], 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_signin_with_unregistered_email(self):
        response = self.client.post(self.signin_url, {'email': 'unregistered@example.com', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
