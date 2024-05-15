from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile_number', 'name']

class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'name']

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['user', 'image', 'action']

