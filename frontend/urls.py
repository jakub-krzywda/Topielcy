from django.urls import include, path
from rest_framework import routers
from .views import index


urlpatterns = [
    path('', index, name='index'),
]
