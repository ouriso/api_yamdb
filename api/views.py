from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsAdmin, NotAuthorReadOnly
from .serializers import (
    UserSerializer,
    AuthSerializer,
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_auth_view(request):
    if 'email' not in request.data or not request.data['email']:
        return Response({"message": "email должен быть введен"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    if User.objects.filter(email=email).exists():
        return Response({"message": "такой email уже существует"}, status=status.HTTP_400_BAD_REQUEST)
    password = get_random_string(length=20)
    username = str(email).split('@')[0]
    user = User.objects.create_user(username=username, email=email, password=password)
    user.email_user(
        subject='Registration',
        message=f'confirmation_code: {password}',
        from_email='from@example.com'
    )
    return Response(
        {"message": "На ваш email направлен код подтверждения"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_token_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email', None)
    confirmation_code = serializer.validated_data.get('confirmation_code', None)
    user = authenticate(email=email, password=confirmation_code)
    if not user:
        return Response({"message": "The data is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({"token": str(refresh.access_token)}, status=status.HTTP_200_OK)


class UserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username',]
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated,
                          IsAdmin,)
