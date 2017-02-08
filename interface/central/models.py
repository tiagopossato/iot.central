from django.db import models

class Log(models.Model):
    tipo = models.CharField(max_length=6)
    mensagem = models.CharField(max_length=255)
    sync = models.BooleanField(default=False)
    tempo = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.mensagem
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

class Configuracoes(models.Model):
    apiKey = models.CharField(max_length=255, null=False)
    authDomain = models.CharField(max_length=255, null=False)
    databaseURL = models.CharField(max_length=255, null=False)
    storageBucket = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    senha = models.CharField(max_length=255, null=False)
    uidCentral = models.CharField(max_length=48, null=False)
    maxAlarmes =  models.IntegerField(null=False)
    portaSerial =  models.CharField(max_length=20, null=False, default='/dev/ttyAMA0')
    taxa = models.IntegerField(null=False, default=115200)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'

class AlarmeTipo(models.Model):
    codigo = models.IntegerField(unique=True, null=False)
    mensagem = models.CharField(max_length=255, unique=True, null=False)
    prioridade = models.IntegerField(null=False)
    def __str__(self):
        return self.mensagem
    class Meta:
        verbose_name = 'Tipo de Alarme'
        verbose_name_plural = 'Tipos de Alarme'
        
class Ambiente(models.Model):
    nome = models.CharField(max_length=255, null=False)
    uid = models.CharField(max_length=48, null=True, blank=True)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'

class Alarme(models.Model):
    uid = models.CharField(max_length=48, null=True, blank=True)
    ativo =models.BooleanField(default=False, null=False)
    tempoAtivacao = models.DateTimeField(null=False)
    syncAtivacao = models.BooleanField(default=False, null=False)
    tempoInativacao = models.DateTimeField(null=True)
    syncInativacao = models.BooleanField(default=False, null=False)

    alarmeTipo = models.ForeignKey(AlarmeTipo, on_delete=models.PROTECT)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.PROTECT)
    def __str__(self):
        return self.alarmeTipo.mensagem
    class Meta:
        verbose_name = 'Alarme'
        verbose_name_plural = 'Alarmes'

class PlacaExpansaoDigital(models.Model):
    idRede = models.IntegerField(null=False, unique=True)
    descricao = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        if(self.descricao!=None):
            return str(self.idRede) + " - " + self.descricao
        else:
            return str(self.idRede) + " - "
    class Meta:
        verbose_name = 'Placa de expansão digital'
        verbose_name_plural = 'Placas de expansão digital'

class EntradaDigital(models.Model):
    class Meta:
        unique_together = (('placaExpansaoDigital', 'numero'),)

    numero = models.IntegerField(null=False)
    nome = models.CharField(max_length=255, null=False)
    estado = models.BooleanField(default=False, null=False)
    updated_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital,\
        to_field='idRede', on_delete=models.PROTECT)
    alarmeTipo = models.ForeignKey(AlarmeTipo, blank=True, null=True,\
    to_field='codigo', on_delete=models.PROTECT)
    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.placaExpansaoDigital.descricao) + " [ " + str(self.numero) + " ]"
    class Meta:
        verbose_name = 'Entrada digital'
        verbose_name_plural = 'Entradas digitais'
