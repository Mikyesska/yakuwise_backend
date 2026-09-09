from rest_framework.routers import DefaultRouter

from .views import ContactoViewSet, ClienteViewSet, ProyectoViewSet

router = DefaultRouter()
router.register(r'contactos', ContactoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'proyectos', ProyectoViewSet)

urlpatterns = router.urls
