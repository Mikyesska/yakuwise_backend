from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Rol
from .serializers import RolSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10  # valor por defecto
    page_size_query_param = 'page_size'  # el front puede enviar ?page_size=20
    max_page_size = 100  # límite máximo para evitar abusos


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre_rol', 'estado']
    ordering_fields = ['id_rol', 'nombre_rol', 'estado']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # aquí aplicas el paginador

    # --- 201 Created ---
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                {"message": "Rol creado exitosamente", "data": response.data},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # --- 400 Bad Request ---
            return Response(
                {"error": "Datos inválidos", "detalles": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # --- 500 Internal Server Error ---
            return Response(
                {"error": "Error interno del servidor", "detalles": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # --- 403 Forbidden ---
    def permission_denied(self, request, message=None, code=None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {"message": "Rol actualizado correctamente", "data": response.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                {"error": "Datos inválidos", "detalles": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": "Error interno del servidor", "detalles": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
