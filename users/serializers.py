# import json

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken


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


class MyTokenObtainPairSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = PasswordField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['confirmation_code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        refresh = self.get_token(self.user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data
