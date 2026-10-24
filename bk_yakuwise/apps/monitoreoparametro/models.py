from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.cliente.models import Proyecto


# Modelo frecuencia de monitoreo
class FrecuenciaMonitoreo(models.Model):
    id_frecuencia = models.AutoField(primary_key=True)
    nombre_frecuencia = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField()

    class Meta:
        db_table = 'frecuencia_monitoreo'
        verbose_name = "Frecuencia de monitoreo"
        verbose_name_plural = "Frecuencias de monitoreo"

    def __str__(self):
        return self.nombre_frecuencia


# Modelo de horario de monitoreo
class HorarioMonitoreo(models.Model):
    id_horario = models.AutoField(primary_key=True)
    nombre_horario = models.CharField(max_length=100)
    abreviatura_horario = models.CharField(max_length=10)
    descripcion_horario = models.TextField(blank=True)
    hora = models.TimeField()
    estado = models.BooleanField()

    class Meta:
        db_table = 'horario_monitoreo'
        verbose_name = "Horario de monitoreo"
        verbose_name_plural = "Horarios de monitoreo"

    def __str__(self):
        return self.nombre_horario


# Modelo tipo de parametro
class TipoParametro(models.Model):
    id_tipo_parametro = models.AutoField(primary_key=True)
    nombre_tipo_parametro = models.CharField(max_length=50)
    estado = models.BooleanField()

    class Meta:
        db_table = 'tipo_parametro'
        verbose_name = "Tipo de parametro"
        verbose_name_plural = "Tipos de parametro"

    def __str__(self):
        return self.nombre_tipo_parametro


# Modelo unidad de medida
class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    nombre_unidad_medida = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=15)
    estado = models.BooleanField()

    class Meta:
        db_table = 'unidad_medida'
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"

    def __str__(self):
        return self.nombre_unidad_medida


# Modelo de parametro
class Parametro(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=100, unique=True)
    abreviatura = models.CharField(max_length=20, null=True, blank=True)
    id_unidad_medida = models.ForeignKey(
        "UnidadMedida", on_delete=models.PROTECT, db_column="id_unidad_medida"
    )
    id_tipo_parametro = models.ForeignKey(
        "TipoParametro", on_delete=models.PROTECT, db_column="id_tipo_parametro"
    )
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "parametro"
        ordering = ["id_parametro"]

    def __str__(self):
        return f"{self.nombre_parametro} ({self.abreviatura})"


# Modelo parametro punto de muestreo
class ParametroPuntoMuestreo(models.Model):
    id_parametro_punto_muestreo = models.AutoField(primary_key=True)
    id_parametro = models.ForeignKey(
        'Parametro', on_delete=models.CASCADE, db_column='id_parametro'
    )
    id_punto_muestreo = models.ForeignKey(
        'PuntoMuestreo', on_delete=models.CASCADE, db_column='id_punto_muestreo'
    )
    id_frecuencia = models.ForeignKey(
        FrecuenciaMonitoreo, on_delete=models.CASCADE, db_column='id_frecuencia'
    )
    id_horario = models.ForeignKey(
        HorarioMonitoreo, on_delete=models.CASCADE, db_column='id_horario'
    )

    class Meta:
        db_table = 'parametro_punto_muestreo'
        verbose_name = "Parametro punto de muestreo"
        verbose_name_plural = "Parametros puntos de muestreo"

    def __str__(self):
        return self.id_parametro_punto_muestreo


# Modelo de monitoreo
class Monitoreo(models.Model):
    id_monitoreo = models.AutoField(primary_key=True)
    valor_monitoreo = models.IntegerField()
    fecha_monitoreo = models.DateTimeField(auto_now_add=True)
    id_parametro_punto_muestreo = models.ForeignKey(
        'ParametroPuntoMuestreo',
        on_delete=models.CASCADE,
        db_column='id_parametro_punto_muestreo',
    )

    class Meta:
        db_table = 'monitoreo'
        verbose_name = "Monitoreo"
        verbose_name_plural = "Monitoreos"

    def __str__(self):
        return self.id_monitoreo


# Modelo tipo de error
class TipoError(models.Model):
    id_tipo_error = models.AutoField(primary_key=True)
    nombre_tipo_error = models.CharField(max_length=150)

    class Meta:
        db_table = 'tipo_error'
        verbose_name = "Tipo de error"
        verbose_name_plural = "Tipos de errores"

    def __str__(self):
        return self.nombre_tipo_error


# Modelo anormalidad
class Anormalidad(models.Model):
    id_anormmalidad = models.AutoField(primary_key=True)
    fecha_anormalidad = models.DateTimeField()
    id_tipo_error = models.ForeignKey(
        'TipoError', on_delete=models.CASCADE, db_column='id_tipo_error'
    )
    id_monitoreo = models.ForeignKey(
        'Monitoreo', on_delete=models.CASCADE, db_column='id_monitoreo'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anormalidad'
        verbose_name = "Anormalidad"
        verbose_name_plural = "Anormalidades"

    def __str__(self):
        return self.id_anormmalidad


# Modelo accion correctiva
class AccionCorrectiva(models.Model):
    id_accion_correctiva = models.AutoField(primary_key=True)
    descripcion = models.TextField(blank=True)
    fecha_accion_correctiva = models.DateTimeField()
    id_anormalidad = models.ForeignKey(
        'Anormalidad', on_delete=models.CASCADE, db_column='id_anormalidad'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accion_correctiva'
        verbose_name = "Accion correctiva"
        verbose_name_plural = "Acciones correctivas"

    def __str__(self):
        return self.id_accion_correctiva


# Modelo tipo de planta
class TipoPlanta(models.Model):
    id_tipo_planta = models.AutoField(primary_key=True)
    nombre_tipo_planta = models.CharField(max_length=250)
    estado = models.BooleanField()

    class Meta:
        db_table = 'tipo_planta'
        verbose_name = "Tipo de planta"
        verbose_name_plural = "Tipos de plantas"
        ordering = ['id_tipo_planta']

    def __str__(self):
        return self.nombre_tipo_planta


# Modelo planta
class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    tipo_planta = models.ForeignKey(
        'TipoPlanta', on_delete=models.CASCADE, db_column='tipo_planta'
    )
    nombre_planta = models.CharField(max_length=300)
    abreviatura_planta = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField()
    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, db_column='proyecto'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'planta'
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"

    def __str__(self):
        return self.nombre_planta


# Modelo etapa
class Etapa(models.Model):
    id_etapa = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(max_length=255)
    imagen_etapa = models.TextField(blank=True)  # ruta/URL; evita base64
    orden = models.PositiveSmallIntegerField(default=1)  # NUEVO
    id_planta = models.ForeignKey(
        "Planta",
        on_delete=models.PROTECT,  # antes CASCADE
        related_name="etapas",
        db_column="id_planta",
    )
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "etapa"
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"
        ordering = ["id_planta", "orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["id_planta", "nombre_etapa"],
                name="uq_etapa_planta_nombre",
            ),
        ]

    def __str__(self):
        return self.nombre_etapa


# Modelo punto de muestreo
class PuntoMuestreo(models.Model):
    id_punto_muestreo = models.AutoField(primary_key=True)
    nombre_punto_muestreo = models.CharField(max_length=255)
    orden = models.PositiveSmallIntegerField(default=1)  # NUEVO
    id_etapa = models.ForeignKey(
        Etapa,
        on_delete=models.PROTECT,  # antes CASCADE
        related_name="puntos_muestreo",
        db_column="id_etapa",
    )
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "punto_muestreo"
        verbose_name = "Punto de muestreo"
        verbose_name_plural = "Puntos de muestreo"
        ordering = ["id_etapa", "orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["id_etapa", "nombre_punto_muestreo"],
                name="uq_punto_etapa_nombre",
            ),
        ]

    def __str__(self):
        return f"{self.id_etapa} – {self.nombre_punto_muestreo}"


# Modelo LimiteParametro: rango permisible de un parámetro en un punto de muestreo.
class LimiteParametro(models.Model):
    class Fuente(models.TextChoices):
        ECA = "ECA", "ECA – DS N° 004-2017-MINAM"
        LMP = "LMP", "LMP – DS N° 003-2010-MINAM"
        TECNICO = "TEC", "Técnico-operativo de la planta"

    id_limite_parametro = models.AutoField(primary_key=True)
    id_parametro = models.ForeignKey(
        Parametro,
        on_delete=models.PROTECT,
        related_name="limites",
        db_column="id_parametro",
    )
    id_punto_muestreo = models.ForeignKey(
        PuntoMuestreo,
        on_delete=models.PROTECT,
        related_name="limites",
        db_column="id_punto_muestreo",
    )
    # Null = sin límite en ese extremo (p. ej. "máx. 35 °C").
    limite_inferior = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    limite_superior = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    fuente = models.CharField(max_length=3, choices=Fuente.choices)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "limite_parametro"
        ordering = ["id_limite_parametro"]
        constraints = [
            models.UniqueConstraint(
                fields=["id_parametro", "id_punto_muestreo"],
                name="uq_limite_parametro_punto",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(limite_inferior__isnull=True)
                    | models.Q(limite_superior__isnull=True)
                    | models.Q(limite_inferior__lte=models.F("limite_superior"))
                ),
                name="ck_limite_inferior_lte_superior",
            ),
        ]

    def __str__(self):
        inf = self.limite_inferior if self.limite_inferior is not None else "—"
        sup = self.limite_superior if self.limite_superior is not None else "—"
        return (
            f"{self.id_parametro.abreviatura} – {self.id_punto_muestreo}: {inf} a {sup}"
        )

    def clean(self):
        if self.limite_inferior is None and self.limite_superior is None:
            raise ValidationError("Debe definir al menos un límite.")

    def esta_fuera_de_rango(self, valor) -> bool:
        """True si el valor medido es una anomalía (dispara alerta)."""
        valor = Decimal(str(valor))
        if self.limite_inferior is not None and valor < self.limite_inferior:
            return True
        if self.limite_superior is not None and valor > self.limite_superior:
            return True
        return False
