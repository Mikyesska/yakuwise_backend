# apps/project/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.security.views import CustomPagination

from .models import Cliente, Contacto, Proyecto
from .serializers import ClienteSerializer, ContactoSerializer, ProyectoSerializer


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.select_related('id_cliente').all()
    serializer_class = ContactoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['estado', 'id_cliente']
    search_fields = [
        'nombres',
        'apellido_paterno',
        'apellido_materno',
        'area',
        'email_contacto',
        'telefono_contacto',
    ]
    ordering_fields = [
        'id_contacto',
        'nombres',
        'apellido_paterno',
        'estado',
        'fecha_creacion',
    ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['estado']
    search_fields = [
        'nombre_cliente',
        'ruc_cliente',
        'email',
        'telefono',
        'direccion',
    ]
    ordering_fields = [
        'id_cliente',
        'nombre_cliente',
        'ruc_cliente',
        'estado',
        'email',
        'telefono',
        'fecha_creacion',
    ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.select_related('id_cliente').all()
    serializer_class = ProyectoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['estado', 'id_cliente']
    search_fields = ['nombre_proyecto', 'id_cliente__nombre_cliente']
    ordering_fields = ['id_proyecto', 'nombre_proyecto', 'estado', 'fecha_creacion']
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
