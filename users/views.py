
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsAuthorOrReadOnly
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    AuthSerializer,
)

User = get_user_model()


@api_view(['POST'])
def user_auth_view(request):
    if 'email' not in request.data or not request.data['email']:
        return Response({"message": "email должен быть введен"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    if User.objects.filter(email=email).exists():
        return Response({"message": "такой email уже существует"}, status=status.HTTP_400_BAD_REQUEST)
    password = get_random_string(length=20)
    username = str(email).split('@')[0]
    user = User._default_manager.create_user(username=username, email=email, password=password)
    user.email_user(
        subject='Registration',
        message=f'confirmation_code: {password}',
        from_email='from@example.com'
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def user_token_view(request):
    serializer = AuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # serializer.save()
    # email = serializer.validated_data.get('email')
    # confirmation_code = serializer.validated_data.get('confirmation_code')
    # user = get_object_or_404(User, email=email)
    # print(user)
    # if not user.check_password(confirmation_code):
    #     return Response({"message": "confirmation_code is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(request.user)
    # token = serializer.validated_data.get('token')
    return Response({"token": str(refresh.access_token)}, status=status.HTTP_200_OK)


class UserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]
    # def get_queryset(self):
    #     queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username',]
    pagination_class = PageNumberPagination
    # permission_classes = [IsAuthenticatedOrReadOnly & IsAdmin]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer