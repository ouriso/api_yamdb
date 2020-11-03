from django.contrib.auth import get_user_model

from rest_framework import serializers

# импортируем свои модели
# from .models import 


User = get_user_model()

# пишем свои сериалайзеры