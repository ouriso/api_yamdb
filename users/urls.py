from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UsersViewSet, basename='users')


urlpatterns = [
    path('v1/auth/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('v1/auth/token/', views.user_token_view, name='token_obtain_pair'),
    path('v1/auth/email/', views.user_auth_view, name='user_auth'),
    path('v1/users/me/', views.UserViewSet.as_view()),
    path('v1/', include(router.urls)),
]