from django.contrib.auth import get_user_model
from rest_framework import serializers

<<<<<<< HEAD
from .models import Category, Comment, Genre, Review, Title


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def __init__(self, slug_field=None, serializer_for_object=None, **kwargs):
        super().__init__(slug_field, **kwargs)
        self.serializer_for_object = serializer_for_object

    def to_representation(self, obj):
        serializer = self.serializer_for_object(instance=obj)
        return serializer.to_representation(obj)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CustomSlugRelatedField(
        slug_field='slug',
        serializer_for_object=CategorySerializer,
        queryset=Category.objects.all(),
    )
    genre = CustomSlugRelatedField(
        slug_field='slug',
        serializer_for_object=GenreSerializer,
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)
=======
# from .models import Comment, Review
>>>>>>> master


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
