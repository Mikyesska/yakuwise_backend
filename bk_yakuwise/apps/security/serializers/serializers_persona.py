from rest_framework import serializers

from ..models import Persona, TipoDocumento


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ['id_tipo_documento', 'nombre_tipo_documento', 'estado']


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            'id_persona',
            'id_tipo_documento',
            'numero_documento',
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'genero',
            'telefono',
            'correo_personal',
            'estado',
        ]
