from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    apiKey = models.CharField(max_length=255, null=False, unique=True)
    authDomain = models.CharField(max_length=255, null=False, unique=True)
    databaseURL = models.CharField(max_length=255, null=False, unique=True)
    storageBucket = models.CharField(max_length=255, null=False, unique=True)
    email = models.CharField(max_length=255, null=False)
    senha = models.CharField(max_length=255, null=False)
    uidCentral = models.CharField(max_length=48, null=False, unique=True)
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

    alarmeTipo = models.ForeignKey(AlarmeTipo, to_field='codigo', on_delete=models.PROTECT)
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
    numero = models.IntegerField(null=False)
    nome = models.CharField(max_length=255, null=False)
    estado = models.BooleanField(default=False, null=False)
    #define em qual estado o alarme será disparado
    triggerAlarme = models.BooleanField(default=False, null=False)
    updated_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital,\
        to_field='idRede', on_delete=models.PROTECT)
    alarmeTipo = models.ForeignKey(AlarmeTipo, blank=True, null=True,\
    to_field='codigo', on_delete=models.PROTECT)
    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('placaExpansaoDigital', 'numero'),)

    def __str__(self):
        return str(self.placaExpansaoDigital.descricao) + " [ " + str(self.numero) + " ]"
    class Meta:
        verbose_name = 'Entrada digital'
        verbose_name_plural = 'Entradas digitais'

class Grandeza(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, null=False, unique=True)
    unidade = models.CharField(max_length=15, null=False, unique=True)
    updated_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)
    
    def __str__(self):
        return str(self.unidade) + ' (' + str(self.nome) + ')'

    class Meta:
        verbose_name = 'Grandeza'
        verbose_name_plural = 'Grandezas'

class Sensor(models.Model):
    idRede = models.IntegerField(null=False, unique=True)
    descricao = models.CharField(max_length=255, unique=True, default='')
    intervaloAtualizacao = models.IntegerField(null=False, default=2)
    intervaloLeitura = models.IntegerField(null=False, default=2)
    updated_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandezas = models.ManyToManyField(Grandeza, through='SensorGrandeza')
    
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)
        self.__original_idRede = self.idRede
        self.__original_intervaloAtualizacao = self.intervaloAtualizacao
        self.__original_intervaloLeitura = self.intervaloLeitura

    def save(self, *args, **kwargs):
        super(Sensor, self).save(*args, **kwargs) # Call the "real" save() method.
        from central.placaBase.placaBase import PlacaBase
        
        if(self.__original_intervaloAtualizacao != self.intervaloAtualizacao):
            PlacaBase.enviaComando(PlacaBase,str(self.__original_idRede),
            'CHANGE_SEND_TIME', str(self.intervaloAtualizacao))

        if(self.__original_intervaloLeitura != self.intervaloLeitura):
            PlacaBase.enviaComando(PlacaBase,str(self.__original_idRede),
            'CHANGE_READ_TIME', str(self.intervaloLeitura))
        if(self.__original_idRede != self.idRede):
            PlacaBase.enviaComando(PlacaBase,str(self.__original_idRede),
            'CHANGE_ID', str(self.idRede))

    def __str__(self):
        return str(self.descricao) + " [ " + str(self.idRede) + " ]"

    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'

class SensorGrandeza(models.Model):
    obs = models.CharField(max_length=255, blank=True, null=True)
    updated_at =  models.DateTimeField(auto_now=True)
    curvaCalibracao = models.CharField(max_length=255)
    sync = models.BooleanField(default=False, null=False)

    grandeza = models.ForeignKey(Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensor, to_field='idRede', on_delete=models.PROTECT)

    #define combinacao unica    
    class Meta:
        unique_together = (('grandeza', 'sensor'),)

    def __str__(self):
        return str(self.sensor.idRede) + " - " + str(self.grandeza)
        
    class Meta:
        verbose_name = 'Grandeza do Sensor'
        verbose_name_plural = 'Grandezas dos Sensores'

class Leitura(models.Model):
    valor = models.FloatField()
    created_at =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandeza = models.ForeignKey(Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensor, to_field='idRede', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.valor) + " " + str(self.grandeza.unidade)
        
    class Meta:
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'