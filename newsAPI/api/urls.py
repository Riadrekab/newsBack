from django.urls import path,re_path

from . import views
from api import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('getNews',views.getNews.as_view())
]
