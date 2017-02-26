from django.contrib import admin

from central.models import Log
from central.models import AlarmeTipo
from central.models import Alarme
from central.models import PlacaExpansaoDigital
from central.models import EntradaDigital
from central.models import Ambiente
from central.models import Configuracoes
from central.models import Grandeza
from central.models import Sensor
from central.models import SensorGrandeza
from central.models import Leitura

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('tipo','mensagem','tempo','sync',)
    list_display = ('tipo','mensagem','tempo',)
    ordering = ('-tempo',)
    list_filter = ('tipo','tempo',)
    list_per_page = 50
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 0:
            return False
        else:
            return True

class AlarmeAdmin(admin.ModelAdmin):
    readonly_fields = ('uid','ativo','alarmeTipo','ambiente','tempoAtivacao','syncAtivacao','tempoInativacao','syncInativacao',)
    list_display = ('alarmeTipo','ativo','ambiente', 'tempoAtivacao','tempoInativacao',)
    list_filter = ('ativo','tempoAtivacao','ambiente','alarmeTipo',)
    ordering = ('-ativo', '-tempoAtivacao',)
    list_per_page = AlarmeTipo.objects.count()
    
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 0:
            return False
        else:
            return True
 
class AlarmeTipoAdmin(admin.ModelAdmin):
    list_display = ('codigo','mensagem','prioridade',)
    ordering = ('codigo',)
    list_per_page = 50

class PlacaExpansaoDigitalAdmin(admin.ModelAdmin):
    list_display = ('descricao','idRede',)
    ordering = ('idRede',)
    list_per_page = 50

class EntradaDigitalAdmin(admin.ModelAdmin):
    list_display = ('nome','numero','placaExpansaoDigital','estado','ambiente','alarmeTipo','triggerAlarme',)
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

# class GrandezaAdmin(admin.ModelAdmin):
#     readonly_fields = ('sync',)
#     list_display = ('nome','unidade','codigo',)
#     ordering = ('codigo',)

class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ('sync',)
    list_display = ('descricao', 'idRede','intervaloAtualizacao','intervaloLeitura',)
    ordering = ('idRede',)

class SensorGrandezaAdmin(admin.ModelAdmin):
    readonly_fields = ('sync',)
    list_display = ('sensor', 'grandeza','curvaCalibracao','obs',)
    ordering = ('sensor',)
    list_filter = ('sensor','grandeza',)


class LeituraAdmin(admin.ModelAdmin):
    readonly_fields = ('valor','created_at','sync','ambiente','grandeza','sensor',)
    list_display = ('sensor','valor','grandeza','created_at','ambiente',)
    list_filter = ('created_at','sensor','ambiente',)
    ordering = ('-created_at','-sensor')
    list_per_page = 20
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 0:
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
#admin.site.register(Grandeza, GrandezaAdmin)
admin.site.register(Sensor,SensorAdmin)
admin.site.register(SensorGrandeza, SensorGrandezaAdmin)
admin.site.register(Leitura, LeituraAdmin)
admin.site.site_header = 'Administração da Central'
admin.site.site_title = 'Central'