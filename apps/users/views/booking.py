from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.serializers.booking_serializer import BookingSerializer
from apps.users.models.booking import Booking

class BookingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if from_date:
            try:
                bookings = bookings.filter(start_date__gte=from_date)
            except ValueError:
                return Response({"error": "Invalid from date"}, status=status.HTTP_400_BAD_REQUEST)

        if to_date:
            try:
                bookings = bookings.filter(end_date__lte=to_date)
            except ValueError:
                return Response({"error": "Invalid to date"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)