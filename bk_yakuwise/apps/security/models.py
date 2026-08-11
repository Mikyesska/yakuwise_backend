from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(nombre_usuario=username)

    def create_user(
        self, nombre_usuario, email_institucional, password=None, **extra_fields
    ):
        """
        Crea y guarda un usuario normal con la contraseña dada.
        """
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es obligatorio')
        if not email_institucional:
            raise ValueError('El email institucional es obligatorio')

        # Establecer estado=True por defecto si no se proporciona
        extra_fields.setdefault('estado', True)

        usuario = self.model(
            nombre_usuario=nombre_usuario,
            email_institucional=email_institucional,
            **extra_fields,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(
        self, nombre_usuario, email_institucional, password=None, **extra_fields
    ):
        """
        Crea y guarda un superusuario con la contraseña dada.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(
            nombre_usuario, email_institucional, password, **extra_fields
        )


# Modelo tipo de documento de identidad
class TipoDocumento(models.Model):
    id_tipo_documento = models.SmallAutoField(primary_key=True)
    nombre_tipo_documento = models.CharField(
        max_length=100, help_text="Ej: Documento nacional de identidad."
    )
    estado = models.BooleanField()

    class Meta:
        db_table = 'tipo_documento'
        # Nombres legibles para humanos en el Admin de Django
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"

    def __str__(self):
        return self.nombre_tipo_documento


# Modelo persona
class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    id_tipo_documento = models.ForeignKey(
        'TipoDocumento',
        on_delete=models.CASCADE,
        db_column='id_tipo_documento',
        null=False,
    )
    numero_documento = models.CharField(
        max_length=20, verbose_name='Numero de documento de identidad'
    )
    nombres = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=150)
    apellido_materno = models.CharField(max_length=150, blank=True, default='')
    genero = models.CharField(max_length=1)
    telefono = models.CharField(max_length=15, blank=True, default='')
    correo_personal = models.CharField(max_length=200)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persona'
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    # Función para obtener el nombre completo de la persona
    def obtener_nombre_completo(self):
        """
        Retorna el nombre completo de la persona, combinando todos los campos.
        """
        # Se usa self.campo para acceder a los valores de la instancia actual
        partes_nombre = [self.nombres, self.apellido_paterno, self.apellido_materno]

        nombre_completo = " ".join(partes_nombre)

        return nombre_completo

    def __str__(self):
        return self.obtener_nombre_completo()


# Modelo usuario
# AbstractBaseUser clase que ofrece django para la gestion de usuarios y contraseñas
class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email_institucional = models.CharField(max_length=255)
    estado = models.BooleanField()
    id_persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, db_column='id_persona', null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    pass_actualizado = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    intentos_fallidos = models.IntegerField(default=0)
    ultimo_intento_fallido = models.DateTimeField(null=True, blank=True)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)

    objects = UsuarioManager()

    # Campos requeridos por AbstractBaseUser
    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email_institucional']

    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.nombre_usuario

    def get_full_name(self):
        """Retorna el nombre completo de la persona asociada."""
        if self.id_persona:
            return self.id_persona.obtener_nombre_completo()
        return self.nombre_usuario

    def get_short_name(self):
        """Retorna el primer nombre de la persona asociada."""
        if self.id_persona:
            return (
                self.id_persona.nombres.split()[0]
                if self.id_persona.nombres
                else self.nombre_usuario
            )
        return self.nombre_usuario

    def get_nombre(self):
        """Retorna el nombre de la persona asociada."""
        if self.id_persona:
            return self.id_persona.nombres
        return self.nombre_usuario

    def get_apellido(self):
        """Retorna el apellido paterno de la persona asociada."""
        if self.id_persona:
            return self.id_persona.apellido_paterno
        return ""

    def get_genero(self):
        """Retorna el género de la persona asociada."""
        if self.id_persona:
            return self.id_persona.genero
        return ""


# Modelo rol
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=150)
    estado = models.BooleanField()

    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre_rol


# Modelo usuariorol
class UsuarioRol(models.Model):
    id_usuario_rol = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column='id_usuario'
    )
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    estado = models.BooleanField()

    class Meta:
        db_table = 'usuario_rol'
        verbose_name = "Usuario rol"
        verbose_name_plural = "Usuarios y roles"

    def __str__(self):
        return self.id_usuario_rol


# Modelo modulo
class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    nombre_modulo = models.CharField(max_length=200)
    estado = models.BooleanField()

    class Meta:
        db_table = 'modulo'
        verbose_name = "Modulo"
        verbose_name_plural = "Modulos"

    def __str__(self):
        return self.nombre_modulo


# Modulo menus
class Menus(models.Model):
    id_menu = models.AutoField(primary_key=True)
    nivel = models.IntegerField()
    orden = models.IntegerField()
    ruta = models.CharField(max_length=250)
    nombre_menu = models.CharField(max_length=250, null=True, blank=True)
    id_modulo = models.ForeignKey(
        'Modulo', on_delete=models.CASCADE, db_column='id_modulo'
    )
    estado = models.BooleanField()

    class Meta:
        db_table = 'menus'
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.id_menu


# Modulo rol_menus
class RolMenus(models.Model):
    id_rol_menus = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    id_menu = models.ForeignKey(Menus, on_delete=models.CASCADE, db_column='id_menu')

    class Meta:
        db_table = 'rol_menus'
        verbose_name = "Rol y menus"
        verbose_name_plural = "Roles y menus"

    def __str__(self):
        return self.id_rol_menus
