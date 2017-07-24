from django.db import models

# Create your models here.

class Mqtt(models.Model):
    STATUS = (
        (0, 'Não configurado'),
        (1, 'Funcionando'),
        (2, 'Falha na comunicação'),
        (3, 'Erro'),
    )
    id =  models.AutoField(primary_key=True)
    status = models.IntegerField('Estado da comunicação', default=0, choices=STATUS)
    descricao = models.CharField('Descrição', null=True, blank=True, max_length=255)
    servidor = models.CharField('Endereço do servidor', null=True, blank=True, max_length=255)
    keyFile = models.TextField('Chave privada',null=True, blank=True)
    certFile = models.TextField('Chave pública',null=True, blank=True)

    class Meta:
        verbose_name = 'Configurações da comunicação MQTT'