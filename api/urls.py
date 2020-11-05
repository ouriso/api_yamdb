from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CommentViewSet, ReviewViewSet


router = DefaultRouter()
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
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/email/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(router.urls)),
]