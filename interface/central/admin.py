from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital
from central.models import Ambiente
from central.models import Configuracoes

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','sync','tempo',)
    list_display = ('tipo','mensagem','tempo','sync',)
    ordering = ('-tempo',)
    list_filter = ('tipo',)

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('tempoAtivacao','ativo','syncAtivacao','tempoInativacao','syncInativacao','alarmeTipo',)
    list_display = ('ativo','alarmeTipo','tempoAtivacao','syncAtivacao','tempoInativacao','syncInativacao',)
    list_filter = ('ativo','tempoAtivacao',)
    ordering = ('-ativo', '-tempoAtivacao',)
    list_per_page = AlarmeTipo.objects.count()
 
class AlarmeTipoAdmin(admin.ModelAdmin):
    list_display = ('codigo','mensagem','prioridade',)
    ordering = ('codigo',)

class PlacaExpansaoDigitalAdmin(admin.ModelAdmin):
    list_display = ('descricao','idRede',)
    ordering = ('idRede',)

class EntradaDigitalAdmin(admin.ModelAdmin):
    list_display = ('placaExpansaoDigital','numero','nome','estado','ambiente','alarmeTipo',)
    ordering = ('placaExpansaoDigital', 'numero',)

class AmbienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uid',)
    ordering = ('nome',)      

class ConfiguracoesAdmin(admin.ModelAdmin):
    list_display = ('apiKey','authDomain','databaseURL',\
                    'storageBucket','email','senha','uidCentral')
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

admin.site.register(Log, LogAdmin)
admin.site.register(AlarmeTipo, AlarmeTipoAdmin)
admin.site.register(Alarme, AlarmeAdmin)
admin.site.register(PlacaExpansaoDigital, PlacaExpansaoDigitalAdmin)
admin.site.register(EntradaDigital, EntradaDigitalAdmin)
admin.site.register(Ambiente, AmbienteAdmin)
admin.site.register(Configuracoes, ConfiguracoesAdmin)