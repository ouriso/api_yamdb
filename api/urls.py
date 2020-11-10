from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    CommentViewSet, ReviewViewSet
)

from users.views import (
    UserViewSet, UsersViewSet
)


router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register(
    'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='title-reviews'
)
router.register(
    'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='review-comments'
)


urlpatterns = [
    path('users/me/', UserViewSet.as_view()),
    path('v1/', include(router.urls)),
]