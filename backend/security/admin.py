from django.contrib import admin
from .models import TipoDoc,Persona, Usuario

# Register your models here.
admin.site.register(TipoDoc)
admin.site.register(Persona)
admin.site.register(Usuario)