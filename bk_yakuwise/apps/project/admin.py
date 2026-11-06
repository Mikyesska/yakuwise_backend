from django.contrib import admin

from .models import Cliente, Contacto, Proyecto

# Register your models here.
admin.site.register(Contacto)
admin.site.register(Cliente)
admin.site.register(Proyecto)
