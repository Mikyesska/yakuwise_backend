from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    LogoutView,
    MenusViewSet,
    MeView,
    ModuloViewSet,
    ResetPasswordCorreoView,
    ResetPasswordView,
    RolMenusViewSet,
    RolViewSet,
    TipoDocumentoViewSet,
    UpdatePasswordView,
    UsuarioViewSet,
)

router = DefaultRouter()
router.register(r'modulos', ModuloViewSet)
router.register(r'menus', MenusViewSet)
router.register(r'rol-menus', RolMenusViewSet)
router.register(r'tipos-documento', TipoDocumentoViewSet, basename='tipodocumento')
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = router.urls + [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path(
        'reset-password-correo/',
        ResetPasswordCorreoView.as_view(),
        name='reset-password-correo',
    ),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
]
