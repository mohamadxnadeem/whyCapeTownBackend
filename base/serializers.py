from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

# ====================================================================


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name=obj.email
        return name

# ====================================================================

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin', 'token','title']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

# ====================================================================

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Experience
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class BlogSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class BnbSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BnBRental
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class VehicleRentalSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VehicleRental
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class BookingSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data















