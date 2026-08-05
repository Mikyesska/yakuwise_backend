import unicodedata

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import serializers

from ..models import Persona, Rol, Usuario, UsuarioRol
from .serializers_persona import PersonaSerializer

ERROR_CREDENCIALES_INVALIDAS = "Credenciales inválidas."
MENSAJE_CREDENCIALES_ACCESO = "Tus credenciales de acceso son:"


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
            'bloqueado_hasta',
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
        """Genera contraseña: prefijo + número de documento."""
        return f"{settings.PASSWORD_PREFIX}{numero_documento}"

    def send_credentials_email(self, usuario, password):
        """Envía email con las credenciales del usuario."""
        try:
            frontend_url = settings.FRONTEND_URL
            login_url = f"{frontend_url}/login"

            subject = "Bienvenido a Yakuwise - Tus credenciales de acceso"
            message = f"""
            Hola {usuario.id_persona.nombres},

            Tu cuenta ha sido creada exitosamente en el sistema Yakuwise.

            {MENSAJE_CREDENCIALES_ACCESO}
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

    def _get_or_create_persona(self, persona_data):
        """Obtiene o crea una persona basada en tipo y número de documento."""
        persona = Persona.objects.filter(
            id_tipo_documento=persona_data.get('id_tipo_documento'),
            numero_documento=persona_data.get('numero_documento'),
        ).first()

        if not persona:
            persona = Persona.objects.create(**persona_data)
        else:
            self._update_persona(persona, persona_data)

        return persona

    def _update_persona(self, persona, persona_data):
        """Actualiza los datos de una persona existente."""
        for attr, value in persona_data.items():
            setattr(persona, attr, value)
        persona.save()

    def _assign_roles(self, usuario, id_roles):
        """Asigna roles a un usuario."""
        if not id_roles:
            return

        UsuarioRol.objects.filter(id_usuario=usuario).delete()
        for rol_id in id_roles:
            try:
                rol = Rol.objects.get(id_rol=rol_id)
                UsuarioRol.objects.create(id_usuario=usuario, id_rol=rol, estado=True)
            except Rol.DoesNotExist:
                raise serializers.ValidationError(f"El rol con id {rol_id} no existe.")

    def create(self, validated_data):
        persona_data = validated_data.pop('id_persona')
        id_roles = validated_data.pop('id_roles', None)

        # Obtener o crear persona
        persona = self._get_or_create_persona(persona_data)

        # Verificar si ya existe un usuario para esta persona
        usuario_existente = Usuario.objects.filter(id_persona=persona).first()
        if usuario_existente:
            self._assign_roles(usuario_existente, id_roles)
            return usuario_existente

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

        # Asignar roles
        self._assign_roles(usuario, id_roles)

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
            self._update_persona(instance.id_persona, persona_data)

        # Actualizar roles si se proporcionan
        if id_roles is not None:
            self._assign_roles(instance, id_roles)

        return instance
