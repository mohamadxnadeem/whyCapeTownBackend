from django.urls import path
from base.views import blogPost_views as views


urlpatterns = [
    # View All:
    path('', views.getBlogs, name='blogs'),
    # View Specific Item based on ID
    path('<str:pk>/', views.getBlog, name='getBlog'),
    # Create, update and delete:
    path('createNewBlog/', views.createBlog, name='createNewBlog'),
    path('update/<str:pk>/', views.updateBlog, name='user-update'),
    path('delete/<str:pk>/', views.deleteBlog, name='user-delete'),
    # Create new review:
    path('<str:pk>/reviews/', views.createBlogReview, name='create-blog-review'),


]