from rest_framework import serializers

from .models import (
    AccionCorrectiva,
    Anormalidad,
    Etapa,
    FrecuenciaMonitoreo,
    HorarioMonitoreo,
    LimiteParametro,
    Monitoreo,
    Parametro,
    ParametroPuntoMuestreo,
    Planta,
    PuntoMuestreo,
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


class LimiteParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimiteParametro
        fields = '__all__'

    def validate(self, data):
        limite_inferior = data.get('limite_inferior')
        limite_superior = data.get('limite_superior')

        if limite_inferior is None and limite_superior is None:
            raise serializers.ValidationError(
                "Debe definir al menos un límite (inferior o superior)."
            )

        if limite_inferior is not None and limite_superior is not None:
            if limite_inferior > limite_superior:
                raise serializers.ValidationError(
                    "El límite inferior no puede ser mayor al límite superior."
                )

        return data


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
