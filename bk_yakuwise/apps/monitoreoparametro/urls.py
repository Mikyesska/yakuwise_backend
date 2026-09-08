from rest_framework.routers import DefaultRouter

from .views import (
    FrecuenciaMonitoreoViewSet,
    HorarioMonitoreoViewSet,
    TipoErrorViewSet,
    TipoParametroViewSet,
    TipoPlantaViewSet,
    UnidadMedidaViewSet,
)

router = DefaultRouter()
router.register(r'frecuencias-monitoreo', FrecuenciaMonitoreoViewSet)
router.register(r'horarios-monitoreo', HorarioMonitoreoViewSet)
router.register(r'tipos-parametro', TipoParametroViewSet)
router.register(r'unidades-medida', UnidadMedidaViewSet)
router.register(r'tipos-error', TipoErrorViewSet)
router.register(r'tipos-planta', TipoPlantaViewSet)

urlpatterns = router.urls
