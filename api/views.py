from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer


@api_view()
def index(request):
    return Response({"message": "Hello, world!"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

# Create your views here.
