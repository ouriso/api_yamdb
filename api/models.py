from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('name', 'slug')
        ordering = ('-name',)


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('name', 'slug')
        ordering = ('-name',)


class Title(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True, default='')
    rating = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles",
                                   db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="titles", db_index=True)

    class Meta:
        ordering = ('-year', '-name',)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        reviews = self.title.reviews
        new_rating = reviews.aggregate(Avg('score'))['score__avg']

        self.title.rating = new_rating
        self.title.save(update_fields=['rating'])


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
