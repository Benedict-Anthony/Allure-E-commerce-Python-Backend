from rest_framework import serializers
from .models import Category, Service, Bookings
 
 
 
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "description",  "image", "slug"]
 
 
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Bookings
        exclude = ["user"]
        
        
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        exclude = ["user"]