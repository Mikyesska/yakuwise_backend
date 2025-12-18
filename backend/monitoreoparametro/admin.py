from django.contrib import admin
from .models import Anormalidad, Etapa, FrecuenciaMonitoreo, HorarioMonitoreo, Monitoreo, ParametroPuntoMuestreo, Parametro, TipoError, TipoPlanta, TipoParametro, PuntoMuestreo, UnidadMedida, Planta, AccionCorrectiva

# Register your models here.
admin.site.register(Anormalidad)
admin.site.register(AccionCorrectiva)
admin.site.register(Etapa)
admin.site.register(FrecuenciaMonitoreo)
admin.site.register(HorarioMonitoreo)
admin.site.register(Monitoreo)
admin.site.register(ParametroPuntoMuestreo)
admin.site.register(PuntoMuestreo)
admin.site.register(Parametro)
admin.site.register(TipoError)
admin.site.register(TipoParametro)
admin.site.register(TipoPlanta)
admin.site.register(Planta)
admin.site.register(UnidadMedida)