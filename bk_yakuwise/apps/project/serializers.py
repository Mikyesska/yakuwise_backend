from rest_framework import serializers

from .models import Cliente, Contacto, Proyecto


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

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

    def _validar_ruc(self, ruc_cliente):
        """Valida el RUC del cliente: 11 dígitos y prefijo 20, 17, 15 o 10."""
        if ruc_cliente:
            if not ruc_cliente.isdigit() or len(ruc_cliente) != 11:
                raise serializers.ValidationError(
                    {
                        'ruc_cliente': (
                            'El RUC debe tener exactamente 11 dígitos numéricos.'
                        )
                    }
                )
            if ruc_cliente[:2] not in ('20', '17', '15', '10'):
                raise serializers.ValidationError(
                    {'ruc_cliente': ('El RUC debe comenzar con 20, 17, 15 o 10.')}
                )

    def validate(self, data):
        telefono = data.get('telefono')
        ruc_cliente = data.get('ruc_cliente')

        self._validar_telefono(telefono)
        self._validar_ruc(ruc_cliente)

        return data


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'
