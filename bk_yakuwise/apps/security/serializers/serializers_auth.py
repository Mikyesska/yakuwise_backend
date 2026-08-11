from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from ..models import Usuario

ERROR_CREDENCIALES_INVALIDAS = "Credenciales inválidas."
ERROR_USUARIO_INACTIVO = "El usuario está inactivo."
ERROR_USUARIO_NO_EXISTE = "El usuario no existe."
ERROR_CAMPO_PASSWORD_REQUERIDO = "Se requiere la contraseña."  # noqa: S2068
ERROR_CAMPO_USUARIO_REQUERIDO = "Se requiere el nombre de usuario."
MENSAJE_CREDENCIALES_ACCESO = "Tus credenciales de acceso son:"


class LoginSerializer(serializers.Serializer):
    nombre_usuario = serializers.CharField()
    password = serializers.CharField()

    def _check_if_user_is_blocked(self, user):
        """Verifica si el usuario está bloqueado."""
        if user.bloqueado_hasta and user.bloqueado_hasta > timezone.now():
            raise serializers.ValidationError(
                {
                    "password": (
                        "Cuenta bloqueada.\n",
                        "Comuníquese con el administrador.",
                    )
                }
            )

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
            raise serializers.ValidationError(
                {
                    "password": (
                        "Cuenta bloqueada.\n",
                        "Comuníquese con el administrador.",
                    )
                }
            )
        elif user.intentos_fallidos == 2:
            user.save()
            raise serializers.ValidationError(
                {
                    "password": (
                        "Le queda un intento. Asegúrese de ingresar la\n"
                        "contraseña correcta o se bloqueará su cuenta."
                    )
                }
            )
        elif user.intentos_fallidos == 1:
            user.save()
            raise serializers.ValidationError(
                {
                    "password": (
                        "Verifique que sus datos\n"
                        "de acceso sean correctos.\n "
                        "Le quedan dos intentos."
                    )
                }
            )

        user.save()
        raise serializers.ValidationError({"password": ERROR_CREDENCIALES_INVALIDAS})

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
                raise serializers.ValidationError(
                    {"password": ERROR_CREDENCIALES_INVALIDAS}
                )

            self._check_if_user_is_blocked(user)
            self._reset_failed_attempts_if_expired(user)

            authenticated_user = authenticate(
                username=nombre_usuario, password=password
            )

            if not authenticated_user:
                self._handle_failed_login(user)

            if not user.estado:
                raise serializers.ValidationError(
                    {"nombre_usuario": ERROR_USUARIO_INACTIVO}
                )

            self._handle_successful_login(user)
            data['user'] = user
            return data

        raise serializers.ValidationError(
            {
                "nombre_usuario": ERROR_CAMPO_USUARIO_REQUERIDO,
                "password": ERROR_CAMPO_PASSWORD_REQUERIDO,
            }
        )


class ResetPasswordSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()

    def validate_id_usuario(self, value):
        try:
            usuario = Usuario.objects.get(id_usuario=value)
            if not usuario.estado:
                raise serializers.ValidationError(ERROR_USUARIO_INACTIVO)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(ERROR_USUARIO_NO_EXISTE)

    def send_reset_password_email(self, usuario, password):
        """Envía email con la nueva contraseña del usuario."""
        try:
            frontend_url = settings.FRONTEND_URL
            login_url = f"{frontend_url}/login"

            subject = "Yakuwise - Contraseña reestablecida"
            message = f"""
            Hola {usuario.id_persona.nombres},

            Tu contraseña ha sido reestablecida exitosamente en el sistema Yakuwise.

            {MENSAJE_CREDENCIALES_ACCESO}
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
        usuario.bloqueado_hasta = None
        usuario.intentos_fallidos = 0
        usuario.usuario_bloqueado = False
        usuario.save()

        # Enviar email con la nueva contraseña
        self.send_reset_password_email(usuario, new_password)

        return usuario


class ResetPasswordCorreoSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    nombre_usuario = serializers.CharField()

    def validate(self, data):
        correo = data.get('correo').strip()
        nombre_usuario = data.get('nombre_usuario').strip()

        try:
            usuario = Usuario.objects.select_related('id_persona').get(
                nombre_usuario=nombre_usuario
            )
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(
                {"nombre_usuario": ERROR_USUARIO_NO_EXISTE}
            )

        if not usuario.estado:
            raise serializers.ValidationError(
                {"nombre_usuario": ERROR_USUARIO_INACTIVO}
            )

        correos_usuario = [
            usuario.email_institucional,
            usuario.id_persona.correo_personal if usuario.id_persona else None,
        ]
        correos_usuario = [c.lower() for c in correos_usuario if c]

        if correo.lower() not in correos_usuario:
            raise serializers.ValidationError(
                {"correo": ("El correo indicado no coincide con el nombre de usuario.")}
            )

        data['usuario'] = usuario
        return data

    def save(self):
        usuario = self.validated_data['usuario']

        # Reutiliza el mismo flujo de reseteo ya existente
        reset_serializer = ResetPasswordSerializer(
            data={'id_usuario': usuario.id_usuario}
        )
        reset_serializer.is_valid(raise_exception=True)
        return reset_serializer.save()


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
