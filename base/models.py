from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200)
    images = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    videos = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reviews = ArrayField(models.CharField(max_length=200), blank=True, default=list)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
