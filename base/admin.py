from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Experience)
admin.site.register(VehicleRental)
admin.site.register(BnBRental)
admin.site.register(Booking)
admin.site.register(BlogPost)
