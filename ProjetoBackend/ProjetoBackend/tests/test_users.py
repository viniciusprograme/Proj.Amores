import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890'
        }

    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(**self.user_data, password='testpass123')
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data, password='testpass123')
        expected = f"{self.user_data['email']} (Test User)"
        self.assertEqual(str(user), expected)


class UserAPITest(APITestCase):
    """Test cases for User API"""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration(self):
        """Test user registration API"""
        url = reverse('users:register')
        response = self.client.post(url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    def test_user_login(self):
        """Test user login API"""
        # First create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        url = reverse('users:login')
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])