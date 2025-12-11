from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users, BioMedicalData, GPSData
from .serializers import UserSerializer, BioMedicalDataSerializer, GPSDataSerializer


@api_view()
def index(request):
    return Response({"message": "Hello, world!"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class BioMedicalDataViewSet(viewsets.ModelViewSet):
    queryset = BioMedicalData.objects.all()
    serializer_class = BioMedicalDataSerializer


class GPSDataViewSet(viewsets.ModelViewSet):
    queryset = GPSData.objects.all()
    serializer_class = GPSDataSerializer

# Create your views here.
