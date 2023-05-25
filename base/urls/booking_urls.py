from django.urls import path
from base.views import booking_views as views


urlpatterns = [
    path('', views.create_booking, name='BookingView'),
   
]