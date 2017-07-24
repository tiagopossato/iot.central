from django.contrib import admin
from comunicacao.models import Mqtt

# Register your models here.
class MqttAdmin(admin.ModelAdmin):
    list_display = ('descricao','servidor','status',)
    readonly_fields = ('keyFile','certFile',)
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True   

admin.site.register(Mqtt, MqttAdmin)
