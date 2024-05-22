#serializers.py
from rest_framework import serializers
from .models import User, Message, FCMToken

class UserSerializer(serializers.ModelSerializer):
    fcm_token = serializers.CharField(write_only=True, required=False)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'photo', 'full_name', 'phone_number', 'position', 'fcm_token']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['title', 'body', 'sender', 'recipient']
