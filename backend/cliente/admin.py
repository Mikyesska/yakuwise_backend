from django.contrib import admin
from .models import Contacto, Cliente, Proyecto

# Register your models here.
admin.site.register(Contacto)
admin.site.register(Cliente)
admin.site.register(Proyecto)