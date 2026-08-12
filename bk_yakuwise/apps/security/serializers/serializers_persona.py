import re

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

    def _validar_numero_documento(self, id_tipo_documento, numero_documento):
        """Valida el número de documento según el tipo de documento."""
        tipo_id = id_tipo_documento.id_tipo_documento

        if tipo_id == 1:
            # DNI: 8 dígitos
            if not numero_documento.isdigit() or len(numero_documento) != 8:
                raise serializers.ValidationError(
                    {
                        'numero_documento': (
                            'Para DNI, el número de documento debe tener '
                            'exactamente 8 dígitos numéricos.'
                        )
                    }
                )
        elif tipo_id in [2, 3]:
            # Carnet de extranjería y Permiso temporal: hasta 12 dígitos
            if not numero_documento.isdigit() or len(numero_documento) > 12:
                raise serializers.ValidationError(
                    {
                        'numero_documento': (
                            'Para este tipo de documento, el número debe tener '
                            'hasta 12 dígitos numéricos.'
                        )
                    }
                )
        elif tipo_id in [4, 5]:
            # Pasaporte y Otros: 9 caracteres alfanuméricos
            if len(numero_documento) != 9 or not re.match(
                r'^[A-Za-z0-9]+$', numero_documento
            ):
                raise serializers.ValidationError(
                    {
                        'numero_documento': (
                            'Para este tipo de documento, el número debe tener '
                            'exactamente 9 caracteres (números y letras).'
                        )
                    }
                )

    def _validar_telefono(self, telefono):
        """Valida el campo teléfono."""
        if telefono and telefono.strip():
            if not telefono.isdigit() or len(telefono) < 7 or len(telefono) > 9:
                raise serializers.ValidationError(
                    {
                        'telefono': (
                            'El teléfono debe tener entre 7 y 9 dígitos numéricos.'
                        )
                    }
                )

    def validate(self, data):
        id_tipo_documento = data.get('id_tipo_documento')
        numero_documento = data.get('numero_documento')
        telefono = data.get('telefono')

        if id_tipo_documento and numero_documento:
            self._validar_numero_documento(id_tipo_documento, numero_documento)

        self._validar_telefono(telefono)

        return data
