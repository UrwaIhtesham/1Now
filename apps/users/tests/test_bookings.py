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

    def test_invalid_id_booking(self):
        data = {
            "vehicle": 4,
            "start_date": "2025-07-20",
            "end_date": "2025-07-22"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_missing_value_booking(self):
        data = {
            "end_date": "2025-07-22"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    '''
    FOR LIST BOOKINGS
    '''

    def test_valid_listing_bookings(self):
        # Create bookings for current user
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date="2025-07-20",
            end_date="2025-07-22"
        )
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date="2025-08-01",
            end_date="2025-08-05"
        )

        response = self.client.get(self.url, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['vehicle'], self.vehicle.id)

    def test_invalid_unauthorised_bookings(self):
        response = self.client.get(self.url, format='json') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_list_bookings_from(self):
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-06-01", 
            end_date="2025-06-05"
        )
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-07-10", 
            end_date="2025-07-15"
        )

        url = f"{self.url}?from=2025-07-01"
        response = self.client.get(url, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_valid_list_bookings_to(self):
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-06-01", 
            end_date="2025-06-05"
        )
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-07-10", 
            end_date="2025-07-15"
        )

        url = f"{self.url}?to=2025-06-30"
        response = self.client.get(url, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_valid_list_bookings_from_and_to(self):
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-06-01", 
            end_date="2025-06-05"
        )
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-07-10", 
            end_date="2025-07-15"
        )
        Booking.objects.create(
            user=self.user, 
            vehicle=self.vehicle, 
            start_date="2025-08-01", 
            end_date="2025-08-05"
        )

        url = f"{self.url}?from=2025-07-01&to=2025-07-30"
        response = self.client.get(url, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)