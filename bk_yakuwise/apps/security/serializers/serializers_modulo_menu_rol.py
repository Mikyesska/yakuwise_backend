from rest_framework import serializers

from ..models import Menus, Modulo, Rol, RolMenus


class ModuloEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['estado']


class MenusEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = ['estado']


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


class ModuloSerializer(serializers.ModelSerializer):
    menus_asociados = serializers.SerializerMethodField()

    class Meta:
        model = Modulo
        fields = ['id_modulo', 'nombre_modulo', 'estado', 'menus_asociados']

    def get_menus_asociados(self, obj):
        menus = Menus.objects.filter(id_modulo=obj.id_modulo, estado=True)
        return [menu.nombre_menu for menu in menus]

    def validate_nombre_modulo(self, value):
        nombre_normalizado = value.strip().lower()

        if self.instance is None:
            if Modulo.objects.filter(nombre_modulo__iexact=nombre_normalizado).exists():
                raise serializers.ValidationError(
                    "Ya existe un módulo con este nombre."
                )
        else:
            if (
                self.instance.nombre_modulo.lower() != nombre_normalizado
                and Modulo.objects.filter(
                    nombre_modulo__iexact=nombre_normalizado
                ).exists()
            ):
                raise serializers.ValidationError(
                    "Ya existe un módulo con este nombre."
                )

        return value


class MenusSerializer(serializers.ModelSerializer):
    nombre_modulo = serializers.CharField(
        source='id_modulo.nombre_modulo', read_only=True
    )
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Menus
        fields = [
            'id_menu',
            'nivel',
            'orden',
            'ruta',
            'nombre_menu',
            'id_modulo',
            'nombre_modulo',
            'id_depende',
            'estado',
            'roles',
        ]

    def get_roles(self, obj):
        rol_menus = RolMenus.objects.filter(id_menu=obj.id_menu)
        return [
            {'id_rol': rm.id_rol.id_rol, 'nombre_rol': rm.id_rol.nombre_rol}
            for rm in rol_menus
        ]

    def validate(self, data):
        nivel = data.get('nivel')
        id_depende = data.get('id_depende')

        # Obtener valores existentes si estamos actualizando
        if self.instance:
            if nivel is None:
                nivel = self.instance.nivel
            if id_depende is None and 'id_depende' not in self.initial_data:
                id_depende = self.instance.id_depende

        # Validar que nivel solo acepte 1 o 2
        if nivel is not None and nivel not in [1, 2]:
            raise serializers.ValidationError(
                {"nivel": "El nivel solo puede ser 1 o 2."}
            )

        # Si el nivel es 1, limpiar id_depende
        if nivel == 1:
            id_depende = None
            data['id_depende'] = None

        # Validar que id_depende sea obligatorio cuando nivel es 2
        if nivel == 2 and not id_depende:
            raise serializers.ValidationError(
                {"id_depende": "El menú padre es requerido cuando el nivel es 2."}
            ) 

        # Validar orden
        if data.get('orden') is not None and data.get('orden') < 1:
            raise serializers.ValidationError(
                {"orden": "El orden debe ser al menos 1."}
            )

        return data


class RolMenusSerializer(serializers.ModelSerializer):
    nombre_rol = serializers.CharField(source='id_rol.nombre_rol', read_only=True)
    nombre_menu = serializers.CharField(source='id_menu.nombre_menu', read_only=True)

    class Meta:
        model = RolMenus
        fields = [
            'id_rol_menus',
            'id_rol',
            'id_menu',
            'nombre_rol',
            'nombre_menu',
        ]

    def validate(self, data):
        id_rol = data.get(
            'id_rol', getattr(self.instance, 'id_rol', None) if self.instance else None
        )
        id_menu = data.get(
            'id_menu',
            getattr(self.instance, 'id_menu', None) if self.instance else None,
        )

        if id_rol and id_menu:
            if RolMenus.objects.filter(id_rol=id_rol, id_menu=id_menu).exists():
                if not self.instance or (
                    self.instance.id_rol != id_rol or self.instance.id_menu != id_menu
                ):
                    raise serializers.ValidationError(
                        "Ya existe una relación entre este rol y menú."
                    )

        return data
