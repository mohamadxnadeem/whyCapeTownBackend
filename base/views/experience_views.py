#====================================================

#Imports

#====================================================

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Experience, Review
from base.serializers import ExperienceSerializer

#====================================================

#Views

#====================================================

@api_view(['GET'])
def getExperiences(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    Experiences = Experience.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(Experiences, 8)

    try:
        Experiences = paginator.page(page)
    except PageNotAnInteger:
        Experiences = paginator.page(1)
    except EmptyPage:
        Experiences = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ExperienceSerializer(Experiences, many=True)
    return Response({
        'Experiences':serializer.data,
        'page':page,
        'pages':paginator.num_pages
    })

#====================================================

@api_view(['GET'])
def getTopExperiences(request):
    experience = Experience.objects.filter(rating__gt=4).order_by('-rating')[0:5]
    serializer = ExperienceSerializer(experience, many=True)
    return Response(serializer.data)

#====================================================

@api_view(['GET'])
def getExperience(request, pk):
    experience = Experience.objects.get(_id=pk)
    serializer = ExperienceSerializer(experience, many=False)
    
    return Response(serializer.data)

#====================================================

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateExperience(request, pk):
    data = request.data
    experience = Experience.objects.get(_id=pk)

    experience.name = data['name']
    experience.images = data['images']
    experience.videos = data['videos']
    experience.price = data['price']
    experience.description = data['description']

    experience.save()

    serializer = ExperienceSerializer(experience, many=False)  
    return Response(serializer.data)

#====================================================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createExperience(request):
    user = request.user

    experience = Experience.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        images='Sample Image',
        videos=0,
        description='',
    )

    serializer = ExperienceSerializer(experience, many=False)
    return Response(serializer.data)

#====================================================

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteExperience(request, pk):
    experience = Experience.objects.get(_id=pk)
    experience.delete()    
    return Response('Experience Deleted')


#====================================================

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    
    return Response('Image was uploaded')

#====================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createExperienceReview(request, pk):
    user = request.user
    experience = Experience.objects.get(_id=pk)
    data = request.data

    #1 - Review already exists
    alreadyExists = experience.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail':'Experience already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #2 - No Raiting or 0
    elif data['rating'] == 0:
        content = {'detail':'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    #3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            experience=experience,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = experience.review_set.all()
        experience.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        experience.rating = total / len(reviews)
        experience.save()

        return Response('Review Added')

#====================================================