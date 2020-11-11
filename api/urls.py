from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')
router.register('users', views.UsersViewSet, basename='users')
router.register(
    'titles/(?P<title_id>[0-9]+)/reviews',
    views.ReviewViewSet,
    basename='title-reviews'
)
router.register(
    'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    views.CommentViewSet,
    basename='review-comments'
)

urlpatterns = [
    path('v1/auth/token/', views.user_token_view, name='token_obtain_pair'),
    path('v1/auth/email/', views.user_auth_view, name='user_auth'),
    path('v1/users/me/', views.UserViewSet.as_view()),
    path('v1/', include(router.urls)),
]
