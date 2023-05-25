from django.urls import path
from base.views import bnbRental_views as views


urlpatterns = [
    # View All:
    path('', views.getBnBs, name='BnBs'),
    # View Specific Item based on ID
    path('<str:pk>/', views.getBnB, name='getBnB'),
    # Create, update and delete:
    path('createNewBnB/', views.createBnB, name='createNewBnB'),
    path('update/<str:pk>/', views.updateBnB, name='user-update'),
    path('delete/<str:pk>/', views.deleteBnB, name='user-delete'),
    # Create new review:
    path('<str:pk>/reviews/', views.createBnBReview, name='create-BnB-review'),


]