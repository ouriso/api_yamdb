from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# from .models import Title, Review
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    # CommentSerializer, ReviewSerializer,
    UserSerializer,
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
    user = User.objects.create(email=email, password=password)
    user.email_user(
        subject='Registration',
        message=f'confirmation_code: {password}',
        from_email='from@example.com'
    )
    return Response(status=status.HTTP_200_OK)


class UserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]

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


# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     # permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]

#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         serializer.save(author=self.request.user, title=title)

#     def get_queryset(self):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         return title.reviews.all()


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     # permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]

#     def get_review(self):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         review = get_object_or_404(
#             Review, title=title, pk=self.kwargs.get('review_id')
#         )
#         return review

#     def perform_create(self, serializer):
#         review = self.get_review()
#         serializer.save(author=self.request.user, review=review)

#     def get_queryset(self):
#         review = self.get_review()
#         return review.comments.all
