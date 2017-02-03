from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital
from central.models import Ambiente
from central.models import Configuracoes

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','tempo','sync',)
    list_display = ('tipo','mensagem','tempo',)
    ordering = ('-tempo',)
    list_filter = ('tipo',)
    list_per_page = 50

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('uid','ativo','alarmeTipo','ambiente','tempoAtivacao','syncAtivacao','tempoInativacao','syncInativacao',)
    list_display = ('ativo','alarmeTipo','ambiente', 'tempoAtivacao','tempoInativacao',)
    list_filter = ('ativo','tempoAtivacao',)
    ordering = ('-ativo', '-tempoAtivacao',)
    list_per_page = AlarmeTipo.objects.count()
 
class AlarmeTipoAdmin(admin.ModelAdmin):
    list_display = ('codigo','mensagem','prioridade',)
    ordering = ('codigo',)
    list_per_page = 50

class PlacaExpansaoDigitalAdmin(admin.ModelAdmin):
    list_display = ('descricao','idRede',)
    ordering = ('idRede',)
    list_per_page = 50

class EntradaDigitalAdmin(admin.ModelAdmin):
    list_display = ('nome','numero','placaExpansaoDigital','estado','ambiente','alarmeTipo',)
    ordering = ('placaExpansaoDigital', 'numero',)
    list_per_page = 50

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