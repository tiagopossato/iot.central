from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('tempoAtivacao','ativo','syncAtivacao','tempoInativacao','syncInativacao','alarmeTipo',)

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','sync','tempo',)


admin.site.register(Log, LogAdmin)
admin.site.register(AlarmeTipo)
admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(PlacaExpansaoDigital)
admin.site.register(EntradaDigital)
