from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models.vehicle import Vehicle
from apps.users.serializers.vehicle_serializer import VehicleSerializer
from django.shortcuts import get_object_or_404

class VehicleUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        vehicle = get_object_or_404(Vehicle, id=id)
        if vehicle.user != request.user:
            return Response({'error': 'You do not have permission to update this vehicle.'}, status= status.HTTP_403_FORBIDDEN)
        
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)