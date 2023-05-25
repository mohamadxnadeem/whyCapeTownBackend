#====================================================

#Imports

#====================================================

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import BnBRental, Review
from base.serializers import BnbSerializer

#====================================================

#Views

#====================================================

@api_view(['GET'])
def getBnBs(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    bnbs = BnBRental.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(bnbs, 8)

    try:
        bnbs = paginator.page(page)
    except PageNotAnInteger:
        bnbs = paginator.page(1)
    except EmptyPage:
        bnbs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = BnbSerializer(bnbs, many=True)
    return Response({
        'bnbs':serializer.data,
        'page':page,
        'pages':paginator.num_pages
    })

#====================================================

@api_view(['GET'])
def getTopBnBs(request):
    bnbs = BnBRental.objects.filter(rating__gt=4).order_by('-rating')[0:5]
    serializer = BnbSerializer(bnbs, many=True)
    return Response(serializer.data)

#====================================================

@api_view(['GET'])
def getBnB(request, pk):
    bnb = BnBRental.objects.get(_id=pk)
    serializer = BnbSerializer(BnBRental, many=False)
    
    return Response(serializer.data)

#====================================================

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateBnB(request, pk):
    data = request.data
    bnb = BnBRental.objects.get(_id=pk)

    bnb.name = data['name']
    bnb.price = data['price']
    bnb.brand = data['brand']
    bnb.countInStock = data['countInStock']
    bnb.category = data['category']
    bnb.description = data['description']

    bnb.save()

    serializer = BnbSerializer(bnb, many=False)  
    return Response(serializer.data)

#====================================================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createBnB(request):
    user = request.user

    BnBRental = BnBRental.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description='',
    )

    serializer = BnbSerializer(bnb, many=False)
    return Response(serializer.data)

#====================================================

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteBnB(request, pk):
    bnb = BnBRental.objects.get(_id=pk)
    bnb.delete()    
    return Response('bnb Deleted')


#====================================================

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    BnBRental_id = data['BnBRental_id']
    BnBRental = BnBRental.objects.get(_id=BnBRental_id)

    BnBRental.image = request.FILES.get('image')
    BnBRental.save()
    
    return Response('Image was uploaded')

#====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createBnBReview(request, pk):
    user = request.user
    bnb = BnBRental.objects.get(_id=pk)
    data = request.data

    #1 - Review already exists
    alreadyExists = BnBRental.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail':'BnBRental already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #2 - No Raiting or 0
    elif data['rating'] == 0:
        content = {'detail':'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    #3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            bnb=bnb,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = bnb.review_set.all()
        bnb.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        BnBRental.rating = total / len(reviews)
        BnBRental.save()

        return Response('Review Added')

#====================================================