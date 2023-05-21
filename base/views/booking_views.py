from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Booking, Item
from .serializers import BookingSerializer
from datetime import timedelta

class BookingView(APIView):
    def post(self, request, format=None):
        # Get the data from the request
        data = request.data.copy()

        # If a user is authenticated, add the user to the data
        if request.user.is_authenticated:
            data.update({'user': request.user.id})

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            item = serializer.validated_data.get('item')

            # Check if this item is already booked for the requested time
            existing_bookings = Booking.objects.filter(item=item).filter(start_date__lt=end_date, end_date__gt=start_date)

            if existing_bookings.exists():
                return Response({"error": "This item is already booked for the requested time period."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate the total price
            num_days = (end_date - start_date).days
            total_price = item.price * num_days

            # Save the booking if there's no conflict
            booking = serializer.save()
            booking.total_price = total_price
            booking.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

