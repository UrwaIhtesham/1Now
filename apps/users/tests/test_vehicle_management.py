from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from apps.users.models.user import CustomUser
from apps.users.models.vehicle import Vehicle
from rest_framework_simplejwt.tokens import RefreshToken

class VehicleManagementTests(APITestCase):
    #Adding initial user for the setup
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
        self.url = f'/api/vehicles/'

    #function to generate token for the user
    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    '''
    FOR VEHICLE REGISTRATION
    '''
    #valid vehicle registration with correct fields and user
    def test_valid_vehicle_registration(self):
        #adding dummy vehicle
        data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2023,
            "plate": "ABC-1234"
        }
        #api endpoint with post method
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        #matching status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #matching counts of vehicle in test db
        self.assertEqual(Vehicle.objects.count(), 1)
        #matching user of vehicle with the dummy user
        self.assertEqual(Vehicle.objects.first().user, self.user)

    #invalid vehicle registration with empty fields
    def test_invalid_vehicle_registration(self):
        #adding dummy vehicle with missing field
        data = {
            "make": "", 
            "model": "Civic",
            "year": 2019,
            "plate": "ABC-123"
        }
        response = self.client.post(self.url, data, format='json', **self.auth_header)
        #matching status code (should be 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('make', response.data)

    #invalid vehicle registration with unauthorised user
    def test_unauthorized_vehicle_registration(self):
        data = {
            "make": "Honda",
            "model": "City",
            "year": 2023,
            "plate": "GHI-789"
        }
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    '''
    FOR VEHICLE UPDATION
    '''
    #valid vehicle updation with correct fields and user
    def test_valid_vehicle_update(self):
        #creating dummy vehicle
        vehicle = Vehicle.objects.create(
            user = self.user,
            make='Toyota',
            model='Yaris',
            year = 2002,
            plate='abc-123'
        )
        url = f'/api/vehicles/{vehicle.id}/'
        #adding dummy data for updation
        data= {
            "make": "Honda",
            "model": "City",
            "year": 2002,
            "plate": 'abc-123'
        }
        response = self.client.put(url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #after updation refresh the db to show changes
        vehicle.refresh_from_db()
        #manual checking of updated vehicle fields
        self.assertEqual(vehicle.make, "Honda")
        self.assertEqual(vehicle.model, "City")

    #invlaid vehicle updation with empty fields
    def test_invalid_vehicle_update(self):
        vehicle = Vehicle.objects.create(
            user = self.user,
            make='Toyota',
            model='Yaris',
            year = 2002,
            plate='abc-123'
        )
        url = f'/api/vehicles/{vehicle.id}/'

        #adding dummy data with empty fields
        data= {
            "make": "",
            "model": "City",
            "year": 2002,
            "plate": 'abc-123'
        }
        response = self.client.put(url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('make', response.data or response.data.get('error'))


    '''
    DELETE THE VEHICLE
    '''

    #valid vehicle deletion with authorised user
    def test_valid_vehicle_delete(self):
        vehicle = Vehicle.objects.create(
            user=self.user,
            make='Suzuki',
            model='Mehran',
            year = 2018,
            plate='ABC-1234'
        )
        url = f'/api/vehicles/{vehicle.id}/'
        #api endpoint delete vehicles/vehicleid
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 0)

    #invalid vehicle deletion with unauthorised user
    def test_invalid_unauthorised_vehicle_delete(self):
        #creating dummy user who didn't create the vehicle
        other_user = CustomUser.objects.create_user(email='ali@google.com', password="hello123!")
        other_token = self.get_access_token(other_user)
        other_auth_header = {'HTTP_AUTHORIZATION': f'Bearer {other_token}'}
        #create vehicle with the pre-created user
        vehicle=Vehicle.objects.create(
            user=self.user,
            make='Suzuki',
            model='Mehran',
            year = 2018,
            plate='ABC-1234'
        )
        url = f'/api/vehicles/{vehicle.id}/'
        response = self.client.delete(url, **other_auth_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Vehicle.objects.count(), 1)

    '''
    GET LISTING
    '''

    #valid vehicle listing with correct fields and authorised user
    def test_valid_vehicle_listing(self):
        vehicle=Vehicle.objects.create(
            user=self.user,
            make='Suzuki',
            model='Mehran',
            year = 2018,
            plate='ABC-1234'
        )
        vehicle1=Vehicle.objects.create(
            user=self.user,
            make='Mercedes',
            model='Benz',
            year = 2020,
            plate='XYZ-0987'
        )

        url= f'/api/vehicles/'
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)