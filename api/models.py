from django.db import models

# Create your models here.

class Categories(models.Model):
    name
    slug
    pass


class Genres(models.Model):
    name
    slug
    pass


class Titles(models.Model):
    cathegory
    genre
    name
    year
    pass
