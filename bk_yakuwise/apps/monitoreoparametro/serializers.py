from rest_framework import serializers

from .models import (
    FrecuenciaMonitoreo,
    HorarioMonitoreo,
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
