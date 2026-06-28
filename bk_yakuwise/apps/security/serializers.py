import unicodedata
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import serializers

from .models import Persona, Rol, TipoDocumento, Usuario, UsuarioRol


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


class UsuarioSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(source='id_persona')
    id_roles = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=False,
    )
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'nombre_usuario',
            'email_institucional',
            'estado',
            'persona',
            'id_roles',
            'roles',
            'fecha_creacion',
            'fecha_modificacion',
        ]
        read_only_fields = [
            'id_usuario',
            'nombre_usuario',
            'fecha_creacion',
            'fecha_modificacion',
        ]

    def get_roles(self, obj):
        """Devuelve la lista de roles del usuario."""
        usuario_roles = UsuarioRol.objects.filter(id_usuario=obj, estado=True)
        roles = []
        for usuario_rol in usuario_roles:
            roles.append(
                {
                    'id_rol': usuario_rol.id_rol.id_rol,
                    'nombre_rol': usuario_rol.id_rol.nombre_rol,
                }
            )
        return roles

    def remove_accents(self, text):
        """Elimina tildes y acentos de un texto."""
        normalized = unicodedata.normalize('NFKD', text)
        return ''.join(c for c in normalized if not unicodedata.combining(c))

    def generate_username(self, nombres, apellido_paterno):
        """Genera username: primera letra del nombre + apellido paterno (sin tildes)."""
        if not nombres or not apellido_paterno:
            raise serializers.ValidationError(
                "Se requieren nombres y apellido paterno para generar el username."
            )

        # Eliminar tildes
        nombres_sin_tildes = self.remove_accents(nombres.strip().lower())
        apellido_sin_tildes = self.remove_accents(apellido_paterno.strip().lower())

        primera_letra = nombres_sin_tildes[0]
        apellido = apellido_sin_tildes
        username = f"{primera_letra}{apellido}"

        # Si el username ya existe, usar nombre_completo.apellido_paterno
        if Usuario.objects.filter(nombre_usuario=username).exists():
            nombre_completo = nombres_sin_tildes.replace(' ', '.')
            username = f"{nombre_completo}.{apellido}"

        return username

    def generate_password(self, numero_documento):
        """Genera contraseña: '01' + número de documento."""
        return f"01{numero_documento}"

    def send_credentials_email(self, usuario, password):
        """Envía email con las credenciales del usuario."""
        try:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
            login_url = f"{frontend_url}/login"

            subject = "Bienvenido a Yakuwise - Tus credenciales de acceso"
            message = f"""
            Hola {usuario.id_persona.nombres},

            Tu cuenta ha sido creada exitosamente en el sistema Yakuwise.

            Tus credenciales de acceso son:
            - Usuario: {usuario.nombre_usuario}
            - Contraseña: {password}

            Puedes acceder al sistema en: {login_url}

            Por seguridad, te recomendamos cambiar tu contraseña
            después del primer inicio de sesión.

            Saludos,
            El equipo de Yakuwise
            """

            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yakuwise.com')
            recipient_list = [
                usuario.id_persona.correo_personal,
                usuario.email_institucional,
            ]

            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            # No fallar la creación del usuario si el email no se envía
            print(f"Error al enviar email de credenciales: {str(e)}")

    def create(self, validated_data):
        persona_data = validated_data.pop('id_persona')
        id_roles = validated_data.pop('id_roles', None)

        # Buscar si ya existe una persona con el mismo tipo y número de documento
        persona = Persona.objects.filter(
            id_tipo_documento=persona_data.get('id_tipo_documento'),
            numero_documento=persona_data.get('numero_documento'),
        ).first()

        if persona:
            # Verificar si ya existe un usuario para esta persona
            usuario_existente = Usuario.objects.filter(id_persona=persona).first()

            if usuario_existente:
                # Actualizar datos de la persona existente
                for attr, value in persona_data.items():
                    setattr(persona, attr, value)
                persona.save()

                # Actualizar roles si se proporcionan
                if id_roles:
                    # Eliminar roles existentes
                    UsuarioRol.objects.filter(id_usuario=usuario_existente).delete()
                    # Crear nuevos roles
                    for rol_id in id_roles:
                        try:
                            rol = Rol.objects.get(id_rol=rol_id)
                            UsuarioRol.objects.create(
                                id_usuario=usuario_existente, id_rol=rol, estado=True
                            )
                        except Rol.DoesNotExist:
                            raise serializers.ValidationError(
                                f"El rol con id {rol_id} no existe."
                            )

                return usuario_existente
            else:
                # Actualizar datos de la persona existente
                for attr, value in persona_data.items():
                    setattr(persona, attr, value)
                persona.save()
        else:
            # Crear nueva Persona
            persona = Persona.objects.create(**persona_data)

        # Generar username
        username = self.generate_username(
            persona_data.get('nombres'), persona_data.get('apellido_paterno')
        )

        # Generar contraseña y encriptar
        password = self.generate_password(persona_data.get('numero_documento'))
        hashed_password = make_password(password)

        # Crear Usuario
        usuario = Usuario.objects.create(
            nombre_usuario=username,
            password=hashed_password,
            id_persona=persona,
            **validated_data,
        )

        # Asignar roles si se proporcionan
        if id_roles:
            for rol_id in id_roles:
                try:
                    rol = Rol.objects.get(id_rol=rol_id)
                    UsuarioRol.objects.create(
                        id_usuario=usuario, id_rol=rol, estado=True
                    )
                except Rol.DoesNotExist:
                    raise serializers.ValidationError(
                        f"El rol con id {rol_id} no existe."
                    )

        # Enviar email con las credenciales
        self.send_credentials_email(usuario, password)

        return usuario

    def update(self, instance, validated_data):
        persona_data = validated_data.pop('id_persona', None)
        id_roles = validated_data.pop('id_roles', None)

        # Actualizar campos del usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar persona si se proporcionan datos
        if persona_data and instance.id_persona:
            for attr, value in persona_data.items():
                setattr(instance.id_persona, attr, value)
            instance.id_persona.save()

        # Actualizar roles si se proporcionan
        if id_roles is not None:
            # Eliminar roles existentes
            UsuarioRol.objects.filter(id_usuario=instance).delete()
            # Crear nuevos roles
            for rol_id in id_roles:
                try:
                    rol = Rol.objects.get(id_rol=rol_id)
                    UsuarioRol.objects.create(
                        id_usuario=instance, id_rol=rol, estado=True
                    )
                except Rol.DoesNotExist:
                    raise serializers.ValidationError(
                        f"El rol con id {rol_id} no existe."
                    )

        return instance


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


class LoginSerializer(serializers.Serializer):
    nombre_usuario = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        nombre_usuario = data.get('nombre_usuario')
        password = data.get('password')

        if nombre_usuario and password:
            # Autenticar usuario
            user = authenticate(username=nombre_usuario, password=password)

            if not user:
                raise serializers.ValidationError("Credenciales inválidas.")

            if not user.estado:
                raise serializers.ValidationError("El usuario está inactivo.")

            # Actualizar last_login
            user.last_login = datetime.now()
            user.save()

            data['user'] = user
            return data

        raise serializers.ValidationError(
            "Se requieren nombre de usuario y contraseña."
        )
