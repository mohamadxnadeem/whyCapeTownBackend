#====================================================

#Imports

#====================================================

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import VehicleRental, Review
from base.serializers import VehicleRentalSerializer

#====================================================

#Views

#====================================================

@api_view(['GET'])
def getVehicles(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    vehicles = VehicleRental.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(vehicles, 8)

    try:
        vehicles = paginator.page(page)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = VehicleRentalSerializer(vehicles, many=True)
    return Response({
        'vehicles':serializer.data,
        'page':page,
        'pages':paginator.num_pages
    })

#====================================================

@api_view(['GET'])
def getTopVehicle(request):
    vehicles = VehicleRental.objects.filter(rating__gt=4).order_by('-rating')[0:5]
    serializer = VehicleRentalSerializer(vehicles, many=True)
    return Response(serializer.data)

#====================================================

@api_view(['GET'])
def getVehicle(request, pk):
    vehicle = VehicleRental.objects.get(id=pk)
    serializer = VehicleRentalSerializer(vehicle, many=False)
    
    return Response(serializer.data)

#====================================================

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateVehicle(request, pk):
    data = request.data
    vehicle = VehicleRental.objects.get(id=pk)

    vehicle.name = data['name']
    vehicle.price = data['price']
    vehicle.brand = data['brand']
    vehicle.countInStock = data['countInStock']
    vehicle.category = data['category']
    vehicle.description = data['description']

    vehicle.save()

    serializer = VehicleRentalSerializer(vehicle, many=False)  
    return Response(serializer.data)

#====================================================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createVehicle(request):
    user = request.user

    vehicle = VehicleRental.objects.create(
        user=user,
        name='Sample Name',
        images='',
        videos='Sample Brand',
        description='',
        price=0,
        reviews='',
    )

    serializer = VehicleRentalSerializer(vehicle, many=False)
    return Response(serializer.data)

#====================================================

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteVehicle(request, pk):
    vehicle = VehicleRental.objects.get(id=pk)
    vehicle.delete()    
    return Response('vehicle Deleted')


#====================================================

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    vehicle_id = data['vehicle_id']
    vehicle = VehicleRental.objects.get(id=vehicle_id)

    vehicle.image = request.FILES.get('image')
    vehicle.save()
    
    return Response('Image was uploaded')

#====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createVehicleReview(request, pk):
    user = request.user
    vehicle = VehicleRental.objects.get(id=pk)
    data = request.data

    #1 - Review already exists
    alreadyExists = VehicleRental.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail':'vehicle already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #2 - No Raiting or 0
    elif data['rating'] == 0:
        content = {'detail':'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    #3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            vehicle=vehicle,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = VehicleRental.review_set.all()
        vehicle.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        vehicle.rating = total / len(reviews)
        vehicle.save()

        return Response('Review Added')

#====================================================