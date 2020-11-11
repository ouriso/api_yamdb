from django.contrib.auth import get_user_model
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
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True, default='')
    rating = models.FloatField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="titles")

    class Meta:
        unique_together = ('name', 'year')
        ordering = ('-year', '-name',)
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=10),
                name="A rating value is valid between 1 and 10",
            )
        ]


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField()
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=10),
                name="A score value is valid between 1 and 10",
            )
        ]

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
