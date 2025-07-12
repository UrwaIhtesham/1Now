from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.users.serializers.user_serializer import RegisterSerializer

class RegisterView(APIView):
    # makes the endpoint public so anyone can register not just logged in users
    permission_classes = [AllowAny]

    #post request
    def post(self, request):
        #passes data from request to serializer
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)