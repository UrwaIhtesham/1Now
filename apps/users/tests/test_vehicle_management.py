from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from apps.users.models.user import CustomUser
from apps.users.models.vehicle import Vehicle
from rest_framework_simplejwt.tokens import RefreshToken

class VehicleManagementTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='umar@google.com',
            password = 'abc123!'
        )
        self.token = self.get_access_token(self.user)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.url = reverse('add-vehicle')

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_valid_vehicle_registration(self):
        data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2023,
            "plate": "ABC-1234"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.first().user, self.user)

    def test_invalid_vehicle_registration(self):
        data = {
            "make": "", 
            "model": "Civic",
            "year": 2019,
            "plate": "ABC-123"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('make', response.data)

    def test_unauthorized_vehicle_registration(self):
        data = {
            "make": "Honda",
            "model": "City",
            "year": 2023,
            "plate": "GHI-789"
        }
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




