from django.db import models

# Modelo contacto
class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    area = models.CharField(max_length=255)
    nombres = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=150)
    apellido_materno = models.CharField(max_length=150)
    email_contacto = models.CharField(max_length=255)
    telefono_contacto = models.CharField(max_length=15)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contacto'
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def obtener_nombre_completo(self):
        partes_nombre_contacto = [
            self.apellido_paterno, 
            self.apellido_materno,
            self.nombres            
        ]

        nombre_completo_contacto = " ".join(partes_nombre_contacto)

        return nombre_completo_contacto

    def __str__(self):
        return self.obtener_nombre_completo()

# Modelo cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=255)
    ruc_cliente = models.CharField(max_length=12, help_text='Registro unico del contribuyente')
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=300)
    estado = models.BooleanField()
    id_contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, db_column='id_contacto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre_cliente
    
# Modelo proyecto
class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre_proyecto = models.TextField()
    estado = models.BooleanField()
    id_cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE, db_column='id_cliente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proyecto'
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.nombre_proyecto
