from django.urls import path
from base.views import vehicleRental_views as views


urlpatterns = [
    # View All:
    path('', views.getVehicles, name='Vehicles'),
    # View Specific Item based on ID
    path('<str:pk>/', views.getVehicle, name='getVehicle'),
    # Create, update and delete:
    path('createNewVehicle/', views.createVehicle, name='createNewVehicle'),
    path('update/<str:pk>/', views.updateVehicle, name='user-update'),
    path('delete/<str:pk>/', views.deleteVehicle, name='user-delete'),
    # Create new review:
    path('<str:pk>/reviews/', views.createVehicleReview, name='create-Vehicle-review'),


]