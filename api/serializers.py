from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'role', 'email')


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    confirmation_code = serializers.CharField(required=True, max_length=20, write_only=True)
