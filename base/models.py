from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



# Create your models here.

class Experience(models.Model):
    name = models.CharField(max_length=200)
    images = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    videos = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reviews = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    def __str__(self):
        return self.name


class VehicleRental(models.Model):
    name = models.CharField(max_length=200)
    images = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    videos = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reviews = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    def __str__(self):
        return self.name


class BnBRental(models.Model):
    name = models.CharField(max_length=200)
    images = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    videos = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reviews = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    content = models.TextField()

    def __str__(self):
        return self.title
