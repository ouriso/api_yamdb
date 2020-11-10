import json

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

    def validate(self, data):
        email = data.get('email', None)
        confirmation_code = data.get('confirmation_code', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required'
            )
        email = BaseUserManager.normalize_email(email)
        if confirmation_code is None:
            raise serializers.ValidationError(
                'A confirmation_code is required'
            )
        print(f'email: {email}; conf: {confirmation_code}')
        user = authenticate(email=email, password=confirmation_code)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        return data

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#     def validate(self, attrs):
#         try:
#             request_data = json.loads(self.context['request'].body)
#         except KeyError:
#             raise serializers.ValidationError('request is incorrect')
#         if 'confirmation_code' in request_data:
#             attrs['password'] = request_data['confirmation_code']
#         else:
#             raise serializers.ValidationError('"confirmation_code" field is required')
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         # data['refresh'] = str(refresh)
#         data['token'] = str(refresh.access_token)

#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)

#         return data