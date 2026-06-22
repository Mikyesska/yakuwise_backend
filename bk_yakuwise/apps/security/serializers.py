from rest_framework import serializers

from .models import Rol


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_rol', 'nombre_rol', 'estado']

    def validate_nombre_rol(self, value):
        nombre_normalizado = value.strip().lower()

        if self.instance is None:
            if Rol.objects.filter(nombre_rol__iexact=nombre_normalizado).exists():
                raise serializers.ValidationError("Ya existe un rol con este nombre.")
        else:
            if (
                self.instance.nombre_rol.lower() != nombre_normalizado
                and Rol.objects.filter(nombre_rol__iexact=nombre_normalizado).exists()
            ):
                raise serializers.ValidationError("Ya existe un rol con este nombre.")

        return value

    def validate(self, data):
        if not data.get('nombre_rol') and data.get('estado') is True:
            raise serializers.ValidationError(
                {"nombre_rol": "Un rol activo debe tener un nombre válido."}
            )
        return data
