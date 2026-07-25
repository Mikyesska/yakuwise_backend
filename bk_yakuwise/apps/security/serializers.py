import unicodedata
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from .models import (
    Menus,
    Modulo,
    Persona,
    Rol,
    RolMenus,
    TipoDocumento,
    Usuario,
    UsuarioRol,
)


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

    def _check_if_user_is_blocked(self, user):
        """Verifica si el usuario está bloqueado."""
        if user.bloqueado_hasta and user.bloqueado_hasta > timezone.now():
            raise serializers.ValidationError("Cuenta bloqueada.")

    def _reset_failed_attempts_if_expired(self, user):
        """Reinicia el contador de intentos fallidos si pasaron 5 minutos."""
        if user.ultimo_intento_fallido:
            tiempo_transcurrido = timezone.now() - user.ultimo_intento_fallido
            if tiempo_transcurrido > timedelta(minutes=5):
                user.intentos_fallidos = 0
                user.ultimo_intento_fallido = None
                user.bloqueado_hasta = None
                user.save()

    def _handle_failed_login(self, user):
        """Maneja un intento de login fallido."""
        user.intentos_fallidos += 1
        user.ultimo_intento_fallido = timezone.now()

        if user.intentos_fallidos >= 3:
            user.bloqueado_hasta = timezone.now() + timedelta(minutes=5)
            user.save()
            raise serializers.ValidationError("Cuenta bloqueada.")
        elif user.intentos_fallidos == 2:
            user.save()
            raise serializers.ValidationError(
                "Le queda 1 intento. Asegurese de ingresar la "
                "contraseña correcta o se bloqueará su cuenta"
            )
        elif user.intentos_fallidos == 1:
            user.save()
            raise serializers.ValidationError("Le quedan dos intentos")

        user.save()
        raise serializers.ValidationError("Credenciales inválidas.")

    def _handle_successful_login(self, user):
        """Maneja un login exitoso, reiniciando contadores."""
        user.intentos_fallidos = 0
        user.ultimo_intento_fallido = None
        user.bloqueado_hasta = None
        user.last_login = datetime.now()
        user.save()

    def validate(self, data):
        nombre_usuario = data.get('nombre_usuario')
        password = data.get('password')

        if nombre_usuario and password:
            try:
                user = Usuario.objects.get(nombre_usuario=nombre_usuario)
            except Usuario.DoesNotExist:
                raise serializers.ValidationError("Credenciales inválidas.")

            self._check_if_user_is_blocked(user)
            self._reset_failed_attempts_if_expired(user)

            authenticated_user = authenticate(
                username=nombre_usuario, password=password
            )

            if not authenticated_user:
                self._handle_failed_login(user)

            if not user.estado:
                raise serializers.ValidationError("El usuario está inactivo.")

            self._handle_successful_login(user)
            data['user'] = user
            return data

        raise serializers.ValidationError(
            "Se requieren nombre de usuario y contraseña."
        )


class ResetPasswordSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()

    def validate_id_usuario(self, value):
        try:
            usuario = Usuario.objects.get(id_usuario=value)
            if not usuario.estado:
                raise serializers.ValidationError("El usuario está inactivo.")
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe.")

    def send_reset_password_email(self, usuario, password):
        """Envía email con la nueva contraseña del usuario."""
        try:
            frontend_url = settings.FRONTEND_URL
            login_url = f"{frontend_url}/login"

            subject = "Yakuwise - Contraseña reestablecida"
            message = f"""
            Hola {usuario.id_persona.nombres},

            Tu contraseña ha sido reestablecida exitosamente en el sistema Yakuwise.

            Tus credenciales de acceso son:
            - Usuario: {usuario.nombre_usuario}
            - Contraseña: {password}

            Puedes acceder al sistema en: {login_url}

            Por seguridad, te recomendamos cambiar tu contraseña
            después del inicio de sesión.

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
            print(f"Error al enviar email de reestablecimiento: {str(e)}")

    def save(self):
        id_usuario = self.validated_data['id_usuario']
        usuario = Usuario.objects.get(id_usuario=id_usuario)

        # Generar nueva contraseña: prefijo + número_documento
        numero_documento = usuario.id_persona.numero_documento
        new_password = f"{settings.PASSWORD_PREFIX}{numero_documento}"

        # Encriptar la nueva contraseña
        hashed_password = make_password(new_password)

        # Actualizar la contraseña del usuario
        usuario.password = hashed_password
        usuario.pass_actualizado = False
        usuario.save()

        # Enviar email con la nueva contraseña
        self.send_reset_password_email(usuario, new_password)

        return usuario


class UpdatePasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nueva = serializers.CharField(write_only=True)
    password_confirmacion = serializers.CharField(write_only=True)

    def validate(self, data):
        password_nueva = data.get('password_nueva')
        password_confirmacion = data.get('password_confirmacion')

        if password_nueva != password_confirmacion:
            raise serializers.ValidationError(
                {"password_confirmacion": settings.ERROR_PASSWORDS_NO_COINCIDEN}
            )

        if len(password_nueva) < settings.MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                {
                    "password_nueva": (
                        f"La contraseña debe tener al menos "
                        f"{settings.MIN_PASSWORD_LENGTH} caracteres."
                    )
                }
            )

        return data

    def validate_password_actual(self, value):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError(settings.ERROR_USUARIO_NO_AUTENTICADO)

        usuario = request.user
        if not usuario.check_password(value):
            raise serializers.ValidationError(settings.ERROR_PASSWORD_INCORRECTA)

        return value

    def save(self):
        request = self.context.get('request')
        usuario = request.user

        password_nueva = self.validated_data['password_nueva']
        usuario.set_password(password_nueva)
        usuario.pass_actualizado = True
        usuario.save()

        return usuario


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id_modulo', 'nombre_modulo', 'estado']

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


class ModuloEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['estado']


class MenusSerializer(serializers.ModelSerializer):
    nombre_modulo = serializers.CharField(
        source='id_modulo.nombre_modulo', read_only=True
    )

    class Meta:
        model = Menus
        fields = [
            'id_menu',
            'nivel',
            'orden',
            'ruta',
            'id_modulo',
            'nombre_modulo',
            'estado',
        ]

    def validate(self, data):
        if data.get('nivel') is not None and data.get('nivel') < 1:
            raise serializers.ValidationError(
                {"nivel": "El nivel debe ser al menos 1."}
            )
        if data.get('orden') is not None and data.get('orden') < 1:
            raise serializers.ValidationError(
                {"orden": "El orden debe ser al menos 1."}
            )
        return data


class MenusEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = ['estado']


class RolMenusSerializer(serializers.ModelSerializer):
    nombre_rol = serializers.CharField(source='id_rol.nombre_rol', read_only=True)
    nombre_menu = serializers.CharField(source='id_menu.ruta', read_only=True)

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
