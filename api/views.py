from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# from .models import Title, Review
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    # CommentSerializer, ReviewSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]

    def get_object(self):
        return self.request.user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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
