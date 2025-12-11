from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, BioMedicalDataViewSet, GPSDataViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'biomedical', BioMedicalDataViewSet)
router.register(r'gps', GPSDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
