from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from apps.users.models import CustomUser

class UserRegistrationTests(APITestCase):
    def test_valid_registration(self):

        response = self.client.post(reverse('register'), {
            "email": "umar@google.com",
            "password": "abc123!@#",
            "mobile_number": "+921234567891"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="umar@google.com").exists())

    def test_unvalid_email_registration(self):
        response = self.client.post(reverse('register'), {
            "email": "umargooglecom",
            "password": "umar123$"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", response.data["email"][0])

    def test_unvalid_password_registration(self):
        response=self.client.post(reverse('register'), {
            "email": "umar@gmail.com",
            "password": "umar123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_existing_email_registration(self):
        CustomUser.objects.create_user(email="umar@google.com", password="umar123!")
        response = self.client.post(reverse('register'), {
            "email": "umar@google.com",
            "password": "hello123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)