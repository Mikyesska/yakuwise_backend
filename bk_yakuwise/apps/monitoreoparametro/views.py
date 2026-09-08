from rest_framework import viewsets

from .models import (
    FrecuenciaMonitoreo,
    HorarioMonitoreo,
    TipoError,
    TipoParametro,
    TipoPlanta,
    UnidadMedida,
)
from .serializers import (
    FrecuenciaMonitoreoSerializer,
    HorarioMonitoreoSerializer,
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
