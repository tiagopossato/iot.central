from django.db import models
from django.db.models.signals import post_save
#from django.dispatch import receiver
from datetime import datetime
import time
import uuid

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
    uidCentral = models.CharField(max_length=48, null=False, unique=True)
    maxAlarmes =  models.IntegerField(null=False)
    portaSerial =  models.CharField(max_length=20, null=False, default='/dev/ttyAMA0')
    taxa = models.IntegerField(null=False, default=115200)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        
class Ambiente(models.Model):
    nome = models.CharField(max_length=255, null=False)
    uid = models.CharField(max_length=48, null=True, blank=True)
    createdAt =  models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    #sobrescreve o método save para adicionar cadastrar no firebase
    def save(self, *args, **kwargs):
        try:
            from central.ambiente import novoAmbienteFirebase, alteraAmbienteFirebase
            if(self.id == None):               
                self.createdAt = datetime.fromtimestamp(time.time())
                self = novoAmbienteFirebase(self)
            elif(self.uid != None):
                self.updatedAt = datetime.fromtimestamp(time.time())
                self = alteraAmbienteFirebase(self)
            if(self):
                super(Ambiente, self).save(*args, **kwargs) # Call the "real" save() method.
        except Exception as e:
            from central.log import log
            log('MOD01.0',str(e))
            return str(e)            

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'

class Alarme(models.Model):
    uid = models.CharField(max_length=48, null=True, blank=True) #usado para o firebase
    codigoAlarme = models.CharField(max_length=36,null=False) #usado para controle entre alarmes digitais a analógicos
    mensagemAlarme = models.CharField(max_length=255, null=False)
    prioridadeAlarme = models.IntegerField(null=False)
    ativo = models.BooleanField(default=False, null=False)
    tempoAtivacao = models.DateTimeField(null=False)
    syncAtivacao = models.BooleanField(default=False, null=False)
    tempoInativacao = models.DateTimeField(null=True)
    syncInativacao = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(Ambiente, on_delete=models.PROTECT)
    def __str__(self):
        return self.mensagemAlarme
    class Meta:
        verbose_name = 'Alarme'
        verbose_name_plural = 'Alarmes'

class PlacaExpansaoDigital(models.Model):
    idRede = models.IntegerField(null=False, unique=True)
    descricao = models.CharField(max_length=255, null=True)
    updatedAt = models.DateTimeField(auto_now=True)
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
    triggerAlarme = models.BooleanField('Estado para alarme', default=False, null=False)
    codigoAlarme = models.CharField(max_length=36, default=None)
    mensagemAlarme = models.CharField('Mensagem do alarme', max_length=255)
    prioridadeAlarme = models.IntegerField('Prioridade do alarme')    
    updatedAt =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital,
        to_field='idRede', on_delete=models.PROTECT, verbose_name='Placa de expansão digital')
    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT)
    
    #sobrescreve o método save para adicionar o valor para o código do alarme
    def save(self, *args, **kwargs):
        if(self.codigoAlarme == None):
            self.codigoAlarme = str(uuid.uuid4())
        super(EntradaDigital, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        unique_together = ('placaExpansaoDigital', 'numero',)
        verbose_name = 'Entrada digital'
        verbose_name_plural = 'Entradas digitais'

    def __str__(self):
        return str(self.placaExpansaoDigital.descricao) + " [ " + str(self.numero) + " ]"

class Grandeza(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, null=False, unique=True)
    unidade = models.CharField(max_length=15, null=False, unique=True)
    updatedAt =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)
    
    def __str__(self):
        return str(self.unidade) + ' (' + str(self.nome) + ')'

    class Meta:
        verbose_name = 'Grandeza'
        verbose_name_plural = 'Grandezas'

class Sensor(models.Model):
    idRede = models.IntegerField(null=False, unique=True)
    uid = models.CharField(max_length=48, null=True, blank=True)
    descricao = models.CharField(max_length=255, unique=True, default='')
    intervaloAtualizacao = models.IntegerField(null=False, default=2)
    intervaloLeitura = models.IntegerField(null=False, default=2)
    createdAt =  models.DateTimeField(auto_now=True)
    updatedAt =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandezas = models.ManyToManyField(Grandeza, through='SensorGrandeza')
    
    def save(self, *args, **kwargs):
        from central.sensor import novoSensorFirebase, alteraSensorFirebase
        if(self.id == None):
            self.createdAt = datetime.fromtimestamp(time.time())
            #salva o sensor no firebase            
            self = novoSensorFirebase(self)
            if(self == False):
                return False
        elif(self.uid != None):
            self.updatedAt = datetime.fromtimestamp(time.time())
            self = alteraSensorFirebase(self)

        if(self):
            # Caso for um update armazena os dados antigos
            if(self.id != None):                
                original_idRede = self.get_previous_by_updatedAt().idRede
                original_intervaloAtualizacao = self.get_previous_by_updatedAt().intervaloAtualizacao
                original_intervaloLeitura = self.get_previous_by_updatedAt().intervaloLeitura

            # Call the "real" save() method.    
            super(Sensor, self).save(*args, **kwargs)

            #altera os dados do sensor na placa física
            try:               

                from central.placaBase.placaBase import PlacaBase
                if(original_intervaloAtualizacao != self.intervaloAtualizacao):
                    PlacaBase.enviaComando(PlacaBase,str(original_idRede),
                    'CHANGE_SEND_TIME', str(self.intervaloAtualizacao))

                if(original_intervaloLeitura != self.intervaloLeitura):
                    PlacaBase.enviaComando(PlacaBase,str(original_idRede),
                    'CHANGE_READ_TIME', str(self.intervaloLeitura))
                if(original_idRede != self.idRede):
                    PlacaBase.enviaComando(PlacaBase,str(original_idRede),
                    'CHANGE_ID', str(self.idRede))
            except Exception as e:
                from central.log import log
                log('MOD02.0',str(e))

    def __str__(self):
        return str(self.descricao) + " [ " + str(self.idRede) + " ]"

    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'

class SensorGrandeza(models.Model):
    obs = models.CharField(max_length=255, blank=True, null=True)
    updatedAt =  models.DateTimeField(auto_now=True)
    curvaCalibracao = models.CharField(max_length=255)
    sync = models.BooleanField(default=False, null=False)

    grandeza = models.ForeignKey(Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensor, to_field='idRede', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # Call the "real" save() method.    
        super(SensorGrandeza, self).save(*args, **kwargs)
        from central.sensor import alteraSensorFirebase
        self.sensor.updatedAt = datetime.fromtimestamp(time.time())
        #salva insere no firebase o relaciomanento do sensor com a grandeza
        alteraSensorFirebase(self.sensor)
        
    class Meta:
        #define combinacao unica   
        unique_together = ('grandeza', 'sensor')
        verbose_name = 'Grandeza do Sensor'
        verbose_name_plural = 'Grandezas dos Sensores'

    def __str__(self):
        return str(self.sensor.idRede) + " - " + str(self.grandeza)

class Leitura(models.Model):
    valor = models.FloatField()
    createdAt =  models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandeza = models.ForeignKey(Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensor, to_field='idRede', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.valor) + " " + str(self.grandeza.unidade) + " Sensor:" + str(self.sensor_id)
        
    class Meta:
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'

class AlarmeAnalogico(models.Model):
    codigoAlarme = models.CharField(primary_key=True, max_length=36)
    mensagemAlarme = models.CharField('Mensagem do alarme', max_length=255)
    prioridadeAlarme = models.IntegerField('Prioridade do alarme')
    valorAlarmeOn = models.FloatField('Valor para ativar o alarme')
    valorAlarmeOff = models.FloatField('Valor para desativar o alarme')
    ambiente = models.ForeignKey(Ambiente, to_field='id', on_delete=models.PROTECT)
    grandeza = models.ForeignKey(Grandeza, to_field='codigo', on_delete=models.PROTECT)

    #sobrescreve o método save para adicionar o valor para o código do alarme
    def save(self, *args, **kwargs):
        if(self.codigoAlarme == None):
	        self.codigoAlarme = str(uuid.uuid4())
        super(AlarmeAnalogico, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        verbose_name = 'Alarme Analógico'
        verbose_name_plural = 'Alarmes Analógicos'
    
    def __str__(self):
        return str(self.mensagemAlarme) + " [on:" + str(self.valorAlarmeOn) + ", off:" + str(self.valorAlarmeOff) + "]"
