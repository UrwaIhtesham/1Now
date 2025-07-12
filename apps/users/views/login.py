from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from apps.users.utils.validators import validate_email, validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            validate_email(email)
            validate_password(password)
        except DjangoValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request, email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status= status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)