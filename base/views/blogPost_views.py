#====================================================

#Imports

#====================================================

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Blog, Review
from base.serializers import BlogSerializer

#====================================================

#Views

#====================================================

@api_view(['GET'])
def getBlogs(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    blogs = Blog.objects.filter(title__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(blogs, 8)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = BlogSerializer(blogs, many=True)
    return Response({
        'blogs':serializer.data,
        'page':page,
        'pages':paginator.num_pages
    })

#====================================================

@api_view(['GET'])
def getTopBlogs(request):
    blogs = Blogs.objects.filter(rating__gt=4).order_by('-rating')[0:5]
    serializer = BlogSerializer(products, many=True)
    return Response(serializer.data)

#====================================================

@api_view(['GET'])
def getBlog(request, pk):
    blog = Blog.objects.get(_id=pk)
    serializer = BlogSerializer(blog, many=False)
    
    return Response(serializer.data)

#====================================================

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateBlog(request, pk):
    data = request.data
    blog = Blog.objects.get(_id=pk)

    blog.title = data['title']
    blog.image = data['image']
    blog.content = data['content']


    blog.save()

    serializer = BlogSerializer(blog, many=False)  
    return Response(serializer.data)

#====================================================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createBlog(request):
    user = request.user

    blog = Blog.objects.create(
        user=user,
        title='Sample Name',
        image='',
        content='Sample Brand',
       
    )

    serializer = BlogSerializer(product, many=False)
    return Response(serializer.data)

#====================================================

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteBlog(request, pk):
    blog = Blog.objects.get(_id=pk)
    blog.delete()    
    return Response('blog Deleted')


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
def createBlogReview(request, pk):
    user = request.user
    blog = Blog.objects.get(_id=pk)
    data = request.data

    #1 - Review already exists
    alreadyExists = blog.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail':'blog already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #2 - No Raiting or 0
    elif data['rating'] == 0:
        content = {'detail':'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    #3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = blog.review_set.all()
        blog.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        blog.rating = total / len(reviews)
        blog.save()

        return Response('Review Added')

#====================================================