from django.contrib.auth import get_user_model
from rest_framework import serializers

# from .models import Comment, Review


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'role', 'email')


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         default=serializers.CurrentUserDefault()
#     )

#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'author', 'pub_date')


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         default=serializers.CurrentUserDefault()
#     )
#     score = serializers.IntegerField(source='score', min_value=1, max_value=10)

#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'author', 'score', 'pub_date')
