from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Movie, Theater, Seats, Booking

class MovieSerializer(serializers.ModelSerializer):
    theaters = serializers.PrimaryKeyRelatedField(many=True, queryset=Theater.objects.all())
    class Meta:
        model = Movie
        fields = '__all__'

class TheaterSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    
    class Meta:
        model = Theater
        fields = '__all__'

class SeatsSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Seats
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        ) 
        return user

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = MovieSerializer()
    seats = SeatsSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'

class LoginSerializer(serializers.Serializer): 
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Username and password do not match")
