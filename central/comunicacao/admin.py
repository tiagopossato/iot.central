from django.contrib import admin
from comunicacao.models import Mqtt

# Register your models here.
class MqttAdmin(admin.ModelAdmin):
    list_display = ('descricao','identificador', 'servidor','status',)
    readonly_fields = ('descricao','servidor','identificador', 'keyFile','certFile','caFile',)

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True   

admin.site.register(Mqtt, MqttAdmin)
