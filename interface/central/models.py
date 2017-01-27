from __future__ import unicode_literals

from django.db import models

class Log(models.Model):
    tipo = models.CharField(max_length=6)
    mensagem = models.CharField(max_length=255)
    sync = models.BooleanField(default=False)
    tempo = models.DateTimeField(auto_now=True)

class AlarmeTipo(models.Model):
    codigo = models.IntegerField(unique=True, null=False)
    mensagem = models.CharField(max_length=255, unique=True, null=False)
    prioridade = models.IntegerField(null=False)

class Alarme(models.Model):
    ativo =models.BooleanField(default=False, null=False)
    tempoAtivacao = models.DateTimeField(null=False)
    syncAtivacao = models.BooleanField(default=False, null=False)
    tempoInativacao = models.DateTimeField(null=True)
    syncInativacao = models.BooleanField(default=False, null=False)

    codigoAlarme = models.ForeignKey(AlarmeTipo)

class PlacaExpansaoDigital(models.Model):
    idRede = models.IntegerField(null=False, unique=True)
    descricao = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class EntradaDigital(models.Model):
    class Meta:
        unique_together = (('placaExpansaoDigital', 'numero'),)

    numero = models.IntegerField(null=False)
    nome = models.CharField(max_length=255, null=False)
    estado = models.BooleanField(default=False, null=False)
    updated_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital)

    codigoAlarme = models.ForeignKey(AlarmeTipo, blank=True, null=True)
