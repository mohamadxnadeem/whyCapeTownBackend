from django.contrib import admin

# Register your models here.
from .models import Item, Booking

admin.site.register(Item)
admin.site.register(Booking)