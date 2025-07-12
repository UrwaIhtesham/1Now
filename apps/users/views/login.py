from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from apps.users.utils.validators import validate_email, validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class LoginView(APIView):
    # makes the endpoint public so anyone can login
    permission_classes = [AllowAny]

    def post(self, request):
        #gets email and password from request
        email = request.data.get('email')
        password = request.data.get('password')

        #validate inputs or throw errors
        try:
            validate_email(email)
            validate_password(password)
        except DjangoValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        #check user's credentials
        user = authenticate(request, email=email, password=password)

        #creates drf token for user
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status= status.HTTP_200_OK)
        #invalid login
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)