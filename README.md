# 1Now Car Rental --Backend API

This is a Django REST Framework-based backend for a car rental platform. It is built as a case study for Decklaration. It provides endpoints for user registration, authentication (JWT), vehicle management (add a vehicle, update a vehicle, delete a vehicle, list the vehicles for a user), and booking management (create a booking, and list the bookings for a user). It includes input validation, and unit tests.

## How to Run the Project
1. Clone the repository
```
git clone https://github.com/UrwaIhtesham/1Now.git
```

2. Create & activate a virtual environment
```
python -m venv venv
venv\Scripts\activate    #On Windows
source venv/bin/activate #On Mac/Linux
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server
```
python manage.py runserver
```

## Authentication 

- For API endpoints except user registration and login, a JWT authentication token is required via djangorestframework-simplejwt
- Include the token in headers like:
```
Authorization: Bearer <access_token>
```

## API Endpoints
1. User Management
- Regiter a new user
- POST method
- /api/register/
```
{
  "email": "test@example.com",
  "password": "Test123!",
  "mobile_number": "03001234567"
}
```

- Login a user
- POST method
- /api/login/
```
{
  "email": "test@example.com",
  "password": "Test123!"
}
```
```
{
  "token": "<jwt_token_here>"
}
```

2. Vehicle Management
- Add a Vehicle
- POST method
- /api/vehicles/
```
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2023,
  "plate": "ABC-123"
}
```

- Update vehicle info
- PUT method
- /api/vehicles/<id>/

- Delete vehicle info
- DELETE method
- /api/vehicles/<id>/

- List the vehicles for the logged in user
- GET method
- /api/vehicles/

3. Booking Management
- Book a vehicle
- POST method
- /api/bookings/
```
{
  "vehicle": 1,
  "start_date": "2025-08-01",
  "end_date": "2025-08-05"
}
```

- List the Booking
- GET method
- /api/bookings/
```
/api/bookings/?from=2025-07-01&to=2025-08-01
```

## Running Unit Tests
- All modules have 5+ unit tests
- Edge cases like overlapping bookings, missing fields, and unauthorised access are tested and successfully flagged as passed.
```
python manage.py test apps.users.tests.test_bookings
python manage.py test apps.users.tests.test_login
python manage.py test apps.users.tests.test_user_registration
python manage.py test apps.users.tests.test_vehicle_management
```

## API Documentation
- Swagger UI: http://localhost:8000/swagger/
- ReDoc UI: http://localhost:8000/redoc/
- swagger.json is also included for Postman import testing

## 1Now Product Context
**What 1Now does:**
1Now is a vehicle rental platform designed to streamline the car booking process not only for customers but also for rental providers. It runs private rentals where renters book directly from your website. No third party marketplace fees is charged. 

**Who it serves:**
It serves individuals or businesses looking for short or long term car rentals. By refering to 1Now, indivduals can maximise earnings, maintain control over their brand and manage bookings on their own terms.

**Frontend Integration:**
This backend provides a modular, secure, and well documented REST API, making it easy to integrate with the frontend such as the React or Next.js app powering LahoreCarRental.com. Use 'http://127.0.0.1:8000/api/{endpoint}/ in the frontend to call that api from the backend.

## Assumptions
- Vehicle owners and booking users are assumed to be the same for simplicity
- JWT tokens must be included in the Authorization header for all protected endpoints (except user registration and user login)
- No admin panel is included
- Dates are in YYYY-MM-DD format.
- Input validation, overlaps etc are handles via custom validators in utils.