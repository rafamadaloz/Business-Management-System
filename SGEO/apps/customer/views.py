from rest_framework import generics
from .serializers import ClientSerializer
from SGEO.apps.customer.models import Client


class ClientsList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer