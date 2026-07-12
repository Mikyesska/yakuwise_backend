from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Rol, TipoDocumento, Usuario
from .serializers import (
    LoginSerializer,
    ResetPasswordSerializer,
    RolSerializer,
    TipoDocumentoSerializer,
    UsuarioSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 10  # valor por defecto
    page_size_query_param = 'page_size'  # el front puede enviar ?page_size=20
    max_page_size = 100  # límite máximo para evitar abusos


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(
                {
                    "message": "Login exitoso",
                    "data": {
                        "id_usuario": user.id_usuario,
                        "nombre_usuario": user.nombre_usuario,
                        "email_institucional": user.email_institucional,
                        "nombre_completo": user.get_full_name(),
                        "last_login": user.last_login,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Credenciales inválidas", "detalles": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {
                    "message": "Contraseña reestablecida exitosamente",
                    "data": {
                        "id_usuario": usuario.id_usuario,
                        "nombre_usuario": usuario.nombre_usuario,
                        "email_institucional": usuario.email_institucional,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Error al reestablecer contraseña", "detalles": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('id_persona').all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'nombre_usuario',
        'email_institucional',
        'id_persona__nombres',
        'id_persona__apellido_paterno',
        'id_persona__apellido_materno',
        'id_persona__numero_documento',
    ]
    ordering_fields = ['id_usuario', 'nombre_usuario', 'fecha_creacion']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                {"message": "Usuario creado exitosamente", "data": response.data},
                status=status.HTTP_201_CREATED,
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

    def permission_denied(self, request, message=None, code=None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {"message": "Usuario actualizado correctamente", "data": response.data},
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


class TipoDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoDocumento.objects.filter(estado=True)
    serializer_class = TipoDocumentoSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"message": "Tipos de documento obtenidos exitosamente", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Error interno del servidor", "detalles": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
