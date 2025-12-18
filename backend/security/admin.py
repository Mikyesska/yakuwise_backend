from django.contrib import admin
from .models import TipoDocumento, Persona, Usuario, Rol, UsuarioRol, Menus, RolMenus, Modulo

# Register your models here.
admin.site.register(TipoDocumento)
admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Modulo)
admin.site.register(UsuarioRol)
admin.site.register(Menus)
admin.site.register(RolMenus)
