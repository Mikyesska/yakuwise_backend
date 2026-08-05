# Serializers reorganizados en módulos separados para mejor mantenimiento
# Este archivo mantiene la compatibilidad con importaciones existentes

from .serializers_auth import (
    LoginSerializer,
    ResetPasswordCorreoSerializer,
    ResetPasswordSerializer,
    UpdatePasswordSerializer,
)
from .serializers_modulo_menu_rol import (
    MenusEstadoSerializer,
    MenusSerializer,
    ModuloEstadoSerializer,
    ModuloSerializer,
    RolMenusSerializer,
    RolSerializer,
)
from .serializers_persona import (
    PersonaSerializer,
    TipoDocumentoSerializer,
)
from .serializers_usuario import UsuarioSerializer

# Exportar todos los serializers para mantener compatibilidad
__all__ = [
    # Base serializers
    'TipoDocumentoSerializer',
    'PersonaSerializer',
    # Modulo, Menu, Rol serializers
    'RolSerializer',
    'ModuloSerializer',
    'MenusSerializer',
    'RolMenusSerializer',
    'ModuloEstadoSerializer',
    'MenusEstadoSerializer',
    # Usuario serializers
    'UsuarioSerializer',
    # Auth serializers
    'LoginSerializer',
    'ResetPasswordSerializer',
    'ResetPasswordCorreoSerializer',
    'UpdatePasswordSerializer',
]
