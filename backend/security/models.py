from django.db import models

# Create your models here.

# Modelo tipo de documento de identidad
class TipoDoc(models.Model):
    id_tipo_doc = models.SmallAutoField(primary_key=True)
    nombre_tipo_doc = models.CharField(max_length=100,help_text=("Nombre del tipo de documento de identidad de una persona."))
    estado = models.BooleanField()

    class Meta:
        db_table = 'tipo_doc'
        # Nombres legibles para humanos en el Admin de Django
        verbose_name = ("Tipo de documento")
        verbose_name_plural = ("Tipos de documentos")
    
    def __str__(self):
        return self.nombre_tipo_doc
    
# Modelo persona
class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    id_tipo_doc = models.ForeignKey('TipoDoc', on_delete=models.CASCADE, db_column='id_tipo_doc')
    numero_doc = models.CharField(max_length=20, verbose_name='Numero de documento de identidad')
    nombres = models.CharField(max_length=150)
    apellido_pat = models.CharField(max_length=150)
    apellido_mat = models.CharField(max_length=150)
    genero = models.CharField(max_length=1)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo_per = models.CharField(max_length=200)
    estado = models.BooleanField()

    class Meta:
        db_table = 'persona'
        verbose_name = ("Persona")
        verbose_name_plural = ("Personas")

    # Función para obtener el nombre completo de la persona
    def obtener_nombre_completo(self):
        """
        Retorna el nombre completo de la persona, combinando todos los campos.
        """
        # Se usa self.campo para acceder a los valores de la instancia actual
        partes_nombre = [
            self.apellido_pat, 
            self.apellido_mat,
            self.nombres            
        ]
        
        nombre_completo = " ".join(partes_nombre)
        
        return nombre_completo
    
    def __str__(self):
        return self.obtener_nombre_completo()
    
# Modelo usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usu = models.CharField(max_length=100,unique=True)
    email_inst = models.CharField(max_length=255)
    estado = models.BooleanField()
    id_persona = models.ForeignKey(Persona,on_delete=models.CASCADE,db_column='id_persona')

    class Meta:
        db_table = 'usuario'
        verbose_name = ("Usuario")
        verbose_name_plural = ("Usuarios")

    def __str__(self):
        return self.nombre_usu