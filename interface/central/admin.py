from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','sync','tempo',)
    list_display = ('tipo','mensagem','tempo','sync',)

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('tempoAtivacao','ativo','syncAtivacao','tempoInativacao','syncInativacao','alarmeTipo',)
    list_display = ('ativo','alarmeTipo','tempoAtivacao','syncAtivacao','tempoInativacao','syncInativacao',)

class AlarmeTipoAdmin(admin.ModelAdmin):
    list_display = ('codigo','mensagem','prioridade',)

class PlacaExpansaoDigitalAdmin(admin.ModelAdmin):
    list_display = ('descricao','idRede',)

class EntradaDigitalAdmin(admin.ModelAdmin):
    list_display = ('numero','nome','estado','sync','placaExpansaoDigital','alarmeTipo',)

admin.site.register(Log, LogAdmin)
admin.site.register(AlarmeTipo, AlarmeTipoAdmin)
admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(PlacaExpansaoDigital, PlacaExpansaoDigitalAdmin)
admin.site.register(EntradaDigital, EntradaDigitalAdmin)
