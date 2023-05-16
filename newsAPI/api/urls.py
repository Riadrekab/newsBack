from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.getRoutes, name="routes"),
    path('users/register/', views.registerUser, name='register'),
    path('users/valid-token/', views.validate_token, name='validate-token'),
    path('users/logout/blacklist/', TokenBlacklistView.as_view(), name='blacklist'),

    path('users/<str:username>/', views.getProfile, name='profile'),
    path('users/update/<str:username>/', views.updateProfile, name='update-profile'),

    path('topics/', views.getTopics, name='topics'),
    path('topics/<str:username>/', views.getProfileTopics, name='topic'),

    path('getNews', views.getNews.as_view())
]
