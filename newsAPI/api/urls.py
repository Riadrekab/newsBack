from django.urls import path, re_path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.getRoutes, name="routes"),
    path('users/register/', views.registerUser, name='register'),
    path('users/login/', views.loginUser, name='login'),
    path('getNews', views.getNews.as_view())
]
