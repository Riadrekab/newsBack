from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('users/register/', views.registerUser, name='register'),
    path('users/login/', views.loginUser, name='login')
]
