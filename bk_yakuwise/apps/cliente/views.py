# apps/cliente/views.py
from rest_framework import viewsets

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    print('si llego a views :)')
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
