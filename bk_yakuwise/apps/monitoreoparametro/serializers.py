from rest_framework import serializers

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


class FrecuenciaMonitoreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrecuenciaMonitoreo
        fields = '__all__'


class HorarioMonitoreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioMonitoreo
        fields = '__all__'


class TipoParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoParametro
        fields = '__all__'


class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'


class TipoErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoError
        fields = '__all__'


class TipoPlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPlanta
        fields = '__all__'


class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = '__all__'


class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'


class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = '__all__'


class PuntoMuestreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoMuestreo
        fields = '__all__'


class ParametroPuntoMuestreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametroPuntoMuestreo
        fields = '__all__'


class MonitoreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoreo
        fields = '__all__'


class AnormalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anormalidad
        fields = '__all__'


class AccionCorrectivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionCorrectiva
        fields = '__all__'
