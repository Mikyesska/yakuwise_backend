# apps/cliente/views.py
from rest_framework import viewsets

from .models import Contacto, Cliente, Proyecto
from .serializers import ContactoSerializer, ClienteSerializer, ProyectoSerializer


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
