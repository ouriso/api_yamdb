import uuid

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrAdminOrModeratorOrReadOnly)
from .serializers import (AdminUserSerializer, AuthSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)

User = get_user_model()


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_auth_view(request):
    email = request.data['email']
    confirmation_code = uuid.uuid4()
    username = email
    user, created = User.objects.get_or_create(
        username=username, email=email, confirmation_code=confirmation_code
    )
    user.email_user(
        subject='Registration',
        message=f'confirmation_code: {confirmation_code}',
    )
    return Response(
        {'message': 'На ваш email направлен код подтверждения'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_token_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    email = data.get('email', None)
    confirmation_code = data.get('confirmation_code', None)

    user = get_object_or_404(User, email=email)
    if user.confirmation_code != confirmation_code:
        return Response({'message': 'The data is incorrect'},
                        status=status.HTTP_400_BAD_REQUEST)
    user.confirmation_code = None
    user.save(['confirmation_code'])

    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    lookup_field = 'username'
    serializer_class = AdminUserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username']
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin]

    @action(
        methods=('get', 'patch'), detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(User, email=self.request.user.email)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        new_role = request.data.get('role')
        new_email = request.data.get('email')
        if new_role and new_role != user.role:
            return Response(
                {'message': 'User can`t change the role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if new_email and new_email != user.email:
            return Response(
                {'message': 'User can`t change the email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GenreViewSet(CreateListDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly &
                          permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly &
                          permissions.IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review, title_id=title_id, pk=review_id
        )

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
