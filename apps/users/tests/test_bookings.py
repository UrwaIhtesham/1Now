from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from apps.users.models.user import CustomUser
from apps.users.models.vehicle import Vehicle
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models.booking import Booking

class BookingTests(APITestCase):
    def setUp(self):
        #adding dummy user
        self.user = CustomUser.objects.create_user(
            email='umar@google.com',
            password = 'abc123!'
        )
        #generating token
        self.token = self.get_access_token(self.user)
        #inserting token to header
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        self.vehicle = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Yaris',
            year=2020,
            plate='ABC-123'
        )

        self.url = f'/api/bookings/'

    #function to generate token for the user
    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    '''
    FOR CREATE BOOKING
    '''
    def test_valid_bookings(self):
        data={
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-20",
            "end_date": "2025-07-22"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_invalid_dates_booking(self):
        data={
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-22",
            "end_date": "2025-07-20"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_overlapped_bookings(self):
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date="2025-07-20",
            end_date="2025-07-25"
        )
        data= {
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-22",
            "end_date": "2025-07-28"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_unauthorised_booking(self):
        data = {
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-20",
            "end_date": "2025-07-22"
        }
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
