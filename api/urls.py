from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


router = DefaultRouter()

router.register('users', views.UsersViewSet, basename='users')
# router.register(
#     'titles/(?P<title_id>[0-9]+)/reviews',
#     views.ReviewViewSet,
#     basename='title-reviews'
# )
# router.register(
#     'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
#     views.CommentViewSet,
#     basename='review-comments'
# )


urlpatterns = [
    # path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/email/', views.user_auth_view, name='user_auth'),
    path('users/me/', views.UserViewSet.as_view()),
    path('v1/', include(router.urls)),
]