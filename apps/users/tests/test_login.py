from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.users.models import CustomUser
from rest_framework.authtoken.models import Token

class LoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="umar@google.com",
            password="abc123!"
        )
    
    def test_valid_login(self):
        response = self.client.post(reverse('login'), {
            "email": "umar@google.com",
            "password": "abc123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_invalid_password_login(self):
        response = self.client.post(reverse('login'), {
            "email": "umar@google.com",
            "password": "abc12345"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)