from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users.models.vehicle import Vehicle
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.serializers.vehicle_serializer import VehicleSerializer

class VehicleCreateView(APIView):
    #the request should be bearing the jwt token or it will throw error
    authentication_classes = [JWTAuthentication]
    #only valid logged in users can access the api
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            #Saves the vehicle and links it to the logged in user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)