from rest_framework import viewsets

from .models import (
    AccionCorrectiva,
    Anormalidad,
    Etapa,
    FrecuenciaMonitoreo,
    HorarioMonitoreo,
    Monitoreo,
    Parametro,
    ParametroPuntoMuestreo,
    PuntoMuestreo,
    Planta,
    TipoError,
    TipoParametro,
    TipoPlanta,
    UnidadMedida,
)
from .serializers import (
    AccionCorrectivaSerializer,
    AnormalidadSerializer,
    EtapaSerializer,
    FrecuenciaMonitoreoSerializer,
    HorarioMonitoreoSerializer,
    MonitoreoSerializer,
    ParametroPuntoMuestreoSerializer,
    ParametroSerializer,
    PlantaSerializer,
    PuntoMuestreoSerializer,
    TipoErrorSerializer,
    TipoParametroSerializer,
    TipoPlantaSerializer,
    UnidadMedidaSerializer,
)


class FrecuenciaMonitoreoViewSet(viewsets.ModelViewSet):
    queryset = FrecuenciaMonitoreo.objects.all()
    serializer_class = FrecuenciaMonitoreoSerializer


class HorarioMonitoreoViewSet(viewsets.ModelViewSet):
    queryset = HorarioMonitoreo.objects.all()
    serializer_class = HorarioMonitoreoSerializer


class TipoParametroViewSet(viewsets.ModelViewSet):
    queryset = TipoParametro.objects.all()
    serializer_class = TipoParametroSerializer


class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer


class TipoErrorViewSet(viewsets.ModelViewSet):
    queryset = TipoError.objects.all()
    serializer_class = TipoErrorSerializer


class TipoPlantaViewSet(viewsets.ModelViewSet):
    queryset = TipoPlanta.objects.all()
    serializer_class = TipoPlantaSerializer


class ParametroViewSet(viewsets.ModelViewSet):
    queryset = Parametro.objects.all()
    serializer_class = ParametroSerializer


class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer


class EtapaViewSet(viewsets.ModelViewSet):
    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer


class PuntoMuestreoViewSet(viewsets.ModelViewSet):
    queryset = PuntoMuestreo.objects.all()
    serializer_class = PuntoMuestreoSerializer


class ParametroPuntoMuestreoViewSet(viewsets.ModelViewSet):
    queryset = ParametroPuntoMuestreo.objects.all()
    serializer_class = ParametroPuntoMuestreoSerializer


class MonitoreoViewSet(viewsets.ModelViewSet):
    queryset = Monitoreo.objects.all()
    serializer_class = MonitoreoSerializer


class AnormalidadViewSet(viewsets.ModelViewSet):
    queryset = Anormalidad.objects.all()
    serializer_class = AnormalidadSerializer


class AccionCorrectivaViewSet(viewsets.ModelViewSet):
    queryset = AccionCorrectiva.objects.all()
    serializer_class = AccionCorrectivaSerializer
