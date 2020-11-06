from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# class Categories(models.Model):
#     name
#     slug
#     pass


# class Genres(models.Model):
#     name
#     slug
#     pass


# class Titles(models.Model):
#     cathegory
#     genre
#     name
#     year
#     pass


# class Review(models.Model):
#     title = models.ForeignKey(Title, on_delete=models.CASCADE,
#                               related_name="reviews")
#     author = models.ForeignKey(User, on_delete=models.CASCADE,
#                                related_name="reviews")
#     score = models.IntegerField()
#     text = models.TextField()
#     pub_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('author', 'title')
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(score__gte=1) & models.Q(score__lte=10),
#                 name="A score value is valid between 1 and 10",
#             )
#         ]


# class Comment(models.Model):
#     review = models.ForeignKey(Review, on_delete=models.CASCADE,
#                                related_name="comments")
#     author = models.ForeignKey(User, on_delete=models.CASCADE,
#                                related_name="comments")
#     text = models.TextField()
#     pub_date = models.DateTimeField(auto_now_add=True)
