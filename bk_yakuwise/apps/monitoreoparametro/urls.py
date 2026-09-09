from rest_framework.routers import DefaultRouter

from .views import (
    AccionCorrectivaViewSet,
    AnormalidadViewSet,
    EtapaViewSet,
    FrecuenciaMonitoreoViewSet,
    HorarioMonitoreoViewSet,
    MonitoreoViewSet,
    ParametroPuntoMuestreoViewSet,
    ParametroViewSet,
    PuntoMuestreoViewSet,
    PlantaViewSet,
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
router.register(r'parametros', ParametroViewSet)
router.register(r'plantas', PlantaViewSet)
router.register(r'etapas', EtapaViewSet)
router.register(r'puntos-muestreo', PuntoMuestreoViewSet)
router.register(r'parametros-punto-muestreo', ParametroPuntoMuestreoViewSet)
router.register(r'monitoreos', MonitoreoViewSet)
router.register(r'anormalidades', AnormalidadViewSet)
router.register(r'acciones-correctivas', AccionCorrectivaViewSet)

urlpatterns = router.urls
