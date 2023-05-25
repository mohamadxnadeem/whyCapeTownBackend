from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from base.models import *
from base.serializers import BookingSerializer
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    user = request.user
    experience_id = request.data.get('experience_id')
    vehicle_rental_id = request.data.get('vehicle_rental_id')
    bnb_rental_id = request.data.get('bnb_rental_id')
    review = request.data.get('review')

    # Create a booking instance
    booking = Booking.objects.create(user=user, review=review)

    # Link booking to experience, if provided
    if experience_id:
        experience = Experience.objects.get(id=experience_id)
        booking.experience = experience
        booking.save()

    # Link booking to vehicle rental, if provided
    if vehicle_rental_id:
        vehicle_rental = VehicleRental.objects.get(id=vehicle_rental_id)
        booking.vehicle_rental = vehicle_rental
        booking.save()

    # Link booking to BnB rental, if provided
    if bnb_rental_id:
        bnb_rental = BnbRental.objects.get(id=bnb_rental_id)
        booking.bnb_rental = bnb_rental
        booking.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data)