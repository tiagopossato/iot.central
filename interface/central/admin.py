from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','sync','tempo',)
    list_display = ('tipo','mensagem','tempo','sync',)
    ordering = ('-tempo',)

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('tempoAtivacao','ativo','syncAtivacao','tempoInativacao','syncInativacao','alarmeTipo',)
    list_display = ('ativo','alarmeTipo','tempoAtivacao','syncAtivacao','tempoInativacao','syncInativacao',)
    list_filter = ('ativo','tempoAtivacao',)
    ordering = ('-ativo', 'tempoAtivacao',)
    list_per_page = 15

class AlarmeTipoAdmin(admin.ModelAdmin):
    list_display = ('codigo','mensagem','prioridade',)
    ordering = ('codigo',)

class PlacaExpansaoDigitalAdmin(admin.ModelAdmin):
    list_display = ('descricao','idRede',)
    ordering = ('idRede',)

class EntradaDigitalAdmin(admin.ModelAdmin):
    list_display = ('placaExpansaoDigital','numero','nome','estado','alarmeTipo',)
    ordering = ('placaExpansaoDigital', 'numero',)

admin.site.register(Log, LogAdmin)
admin.site.register(AlarmeTipo, AlarmeTipoAdmin)
admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(PlacaExpansaoDigital, PlacaExpansaoDigitalAdmin)
admin.site.register(EntradaDigital, EntradaDigitalAdmin)
