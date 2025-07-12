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
        #get the vehicle in the request or 404 error
        vehicle = get_object_or_404(Vehicle, id=id)
        #if vehicle does not belong to the login user then throw error
        if vehicle.user != request.user:
            return Response({'error': 'You do not have permission to update this vehicle.'}, status= status.HTTP_403_FORBIDDEN)
        
        #existing and new data
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehicleDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        #get the vehicle object or return 404 error
        vehicle = get_object_or_404(Vehicle, id=id)

        #only allowing the owner to delete the vehicle
        if vehicle.user != request.user:
            return Response({'error': 'You do not have permission to delete this vehicle'}, status=status.HTTP_403_FORBIDDEN)
        
        vehicle.delete()
        return Response({'message': 'Vehicle deleted successfully'}, status=status.HTTP_204_NO_CONTENT)