from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
from time import time
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
    uidCentral = models.CharField(max_length=48, null=False, unique=True)
    maxAlarmes = models.IntegerField(null=False)
    portaSerial = models.CharField(
        max_length=20, null=False, default='/dev/ttyAMA0')
    taxa = models.IntegerField(null=False, default=115200)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'


class Ambiente(models.Model):
    nome = models.CharField(max_length=255, null=False)
    uid = models.CharField(max_length=48, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    # sobrescreve o método save para adicionar cadastrar no firebase
    def save(self, *args, **kwargs):
        try:
            from central.ambiente import novoAmbienteFirebase, alteraAmbienteFirebase
            if(self.id == None):
                self.createdAt = datetime.fromtimestamp(time())
                self = novoAmbienteFirebase(self)
            elif(self.uid != None):
                self.updatedAt = datetime.fromtimestamp(time())
                self = alteraAmbienteFirebase(self)
            if(self):
                # Call the "real" save() method.
                super(Ambiente, self).save(*args, **kwargs)
        except Exception as e:
            from central.log import log
            log('MOD01.0', str(e))
            return str(e)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'


class Alarme(models.Model):
    uid = models.CharField(max_length=48, null=True,
                           blank=True)  # usado para o
    # usado para controle entre alarmes digitais a analógicos
    codigoAlarme = models.CharField(max_length=36, null=False)
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

    def __init__(self, *args, **kwargs):
        super(PlacaExpansaoDigital, self).__init__(*args, **kwargs)
        self.original_idRede = self.idRede

    def save(self, *args, **kwargs):
        if(self.id != None):
            self.updatedAt = datetime.fromtimestamp(time())

        # Call the "real" save() method.
        super(PlacaExpansaoDigital, self).save(*args, **kwargs)

        # altera os dados da placa na placa física
        try:
            if(self.id != None):
                from central.placaBase.placaBase import PlacaBase
                if(self.original_idRede != self.idRede):
                    PlacaBase.enviaComando(str(self.original_idRede),
                                           'CHANGE_ID', str(self.idRede))
                    # altera os relacionamentos das entradas digitais
                    ed = EntradaDigital.objects.filter(
                        placaExpansaoDigital_id=self.original_idRede).all()
                    for x in range(len(ed)):
                        ed[x].placaExpansaoDigital_id = self.idRede
                        ed[x].save()

                    # altera os relacionamentos das saidas digitais
                    sd = SaidaDigital.objects.filter(
                        placaExpansaoDigital_id=self.original_idRede).all()
                    for x in range(len(sd)):
                        sd[x].placaExpansaoDigital_id = self.idRede
                        sd[x].save()

        except Exception as e:
            from central.log import log
            log('MOD02.0', str(e))

    def __str__(self):
        if(self.descricao != None):
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
    # define em qual estado o alarme será disparado
    triggerAlarme = models.BooleanField(
        'Estado para alarme', default=False, null=False)
    codigoAlarme = models.CharField(max_length=36, default=None)
    mensagemAlarme = models.CharField('Mensagem do alarme', max_length=255)
    prioridadeAlarme = models.IntegerField('Prioridade do alarme')
    updatedAt = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital,
                                             to_field='idRede', on_delete=models.PROTECT,
                                             verbose_name='Placa de expansão digital')
    ambiente = models.ForeignKey(
        Ambiente, to_field='id', on_delete=models.PROTECT)

    # sobrescreve o método save para adicionar o valor para o código do alarme
    def save(self, *args, **kwargs):
        if(self.codigoAlarme == None):
            self.codigoAlarme = str(uuid.uuid4())
        # Call the "real" save() method.
        super(EntradaDigital, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('placaExpansaoDigital', 'numero',)
        verbose_name = 'Entrada digital'
        verbose_name_plural = 'Entradas digitais'

    def __str__(self):
        return str(self.placaExpansaoDigital.descricao) + " [ " + str(self.numero) + " ]"


class SaidaDigital(models.Model):
    numero = models.IntegerField(null=False)
    nome = models.CharField(max_length=255, null=False)
    ativa = models.BooleanField(default=False, null=False)
    estado = models.BooleanField(default=False, null=False)
    #tempoLigado = models.IntegerField('Tempo ligado em segundos', null=False)
    # tempoDesligado = models.IntegerField(
    #    'Tempo desligado em segundos', null=False)
    updatedAt = models.DateTimeField(auto_now=True)
    ultimoAcionamento = models.DateTimeField(null=True)
    sync = models.BooleanField(default=False, null=False)

    placaExpansaoDigital = models.ForeignKey(PlacaExpansaoDigital,
                                             to_field='idRede', on_delete=models.PROTECT, verbose_name='Placa de expansão digital')

    ambiente = models.ForeignKey(
        Ambiente, to_field='id', on_delete=models.PROTECT)

    def __init__(self, *args, **kwargs):
        super(SaidaDigital, self).__init__(*args, **kwargs)
        self.estadoAnterior = self.estado

    # sobrescreve o método save para adicionar o valor para o código do alarme
    def save(self, *args, **kwargs):
        if (not self.ativa):
            self.estado = False

        # Call the "real" save() method.
        super(SaidaDigital, self).save(*args, **kwargs)

        if(self.estadoAnterior != self.estado):
            if(self.estado):
                self.ligar()
            else:
                self.desligar()

    def ligar(self):
        try:
            if(self.estado == False):
                self.estado = True
                self.ultimoAcionamento = datetime.fromtimestamp(time())
                self.save()
        except Exception as e:
            print(e)
        # liga a saida digital
        from central.placaBase.placaBase import PlacaBase
        from central.log import log
        PlacaBase.enviaComando(idRede=self.placaExpansaoDigital.idRede,
                               tipoGrandeza='SAIDA_DIGITAL', grandeza=self.numero, valor=int(True))
        #log('SDG01.0', "Ligando saida: " + str(self.numero))

    def desligar(self):
        if(self.estado == True):
            self.estado = False
            self.save()
        # desliga a saida digital
        from central.placaBase.placaBase import PlacaBase
        from central.log import log
        PlacaBase.enviaComando(idRede=self.placaExpansaoDigital.idRede,
                               tipoGrandeza='SAIDA_DIGITAL', grandeza=self.numero, valor=int(False))
        #log('SDG01.1', "Desligando saida: " + str(self.numero))

    class Meta:
        unique_together = ('placaExpansaoDigital', 'numero',
                           )  # cria chave primaria composta
        verbose_name = 'Saida digital'
        verbose_name_plural = 'Saidas digitais'

    def __str__(self):
        return str(self.placaExpansaoDigital.descricao) + " [ " + str(self.numero) + " ]"


class Temporizador(models.Model):
    horaLigar = models.TimeField("Hora de ligar", null=False)
    horaDesligar = models.TimeField("Hora de desligar", null=False)
    saidaDigital = models.ForeignKey(SaidaDigital, on_delete=models.PROTECT)

    # sobrescreve o método save para validar a entrada
    def save(self, *args, **kwargs):
        if(self.horaDesligar < self.horaLigar):
            print("Hora de desligar menor que hora de ligar!")
            return False
        try:
            t = Temporizador.objects.filter(
                saidaDigital_id=self.saidaDigital).order_by('horaLigar').all()
            if(len(t) > 0):
                # valida entradas invalidas na esquerda
                for x in range(len(t)):
                    if(self.id == t[x].id):
                        continue
                    if(self.horaLigar <= t[x].horaDesligar):
                        if(self.horaDesligar >= t[x].horaLigar):
                            print(
                                "Entrada invalida: " + str(self.horaDesligar) + " >= " + str(t[x].horaLigar))
                            return False
        except Exception as e:
            print("Erro ao validar o Temporizador: " + str(e))
            return

        # Call the "real" save() method.
        super(Temporizador, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Temporizador'
        verbose_name_plural = 'Temporizadores'


class Grandeza(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, null=False, unique=True)
    unidade = models.CharField(max_length=15, null=False, unique=True)
    updatedAt = models.DateTimeField(auto_now=True)
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
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(
        Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandezas = models.ManyToManyField(Grandeza, through='SensorGrandeza')

    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)
        self.original_idRede = self.idRede
        self.original_intervaloAtualizacao = self.intervaloAtualizacao
        self.original_intervaloLeitura = self.intervaloLeitura

    def save(self, *args, **kwargs):
        from central.sensor import novoSensorFirebase, alteraSensorFirebase
        if(self.id == None):
            self.createdAt = datetime.fromtimestamp(time())
            # salva o sensor no firebase
            self = novoSensorFirebase(self)
            if(self == False):
                return False
        elif(self.uid != None):
            self.updatedAt = datetime.fromtimestamp(time())
            self = alteraSensorFirebase(self)

        if(self):
            # Caso for um update armazena os dados antigos
            if(self.id != None):
                original_idRede = self.get_previous_by_updatedAt().idRede
                original_intervaloAtualizacao = self.get_previous_by_updatedAt().intervaloAtualizacao
                original_intervaloLeitura = self.get_previous_by_updatedAt().intervaloLeitura

            # Call the "real" save() method.
            super(Sensor, self).save(*args, **kwargs)

            # altera os dados do sensor na placa física
            try:
                if(self.id != None):
                    from central.placaBase.placaBase import PlacaBase
                    if(original_intervaloAtualizacao != self.intervaloAtualizacao):
                        PlacaBase.enviaComando(idRede=str(original_idRede),
                                               tipoGrandeza='ESPECIAL', grandeza='INTERVALO_ENVIO',
                                               valor=str(self.intervaloAtualizacao))

                    if(original_intervaloLeitura != self.intervaloLeitura):
                        PlacaBase.enviaComando(idRede=str(original_idRede),
                                               tipoGrandeza='ESPECIAL', grandeza='INTERVALO_ENVIO',
                                               valor=str(self.intervaloLeitura))

                    if(original_idRede != self.idRede):
                        PlacaBase.enviaComando(idRede=str(original_idRede),
                                               tipoGrandeza='ESPECIAL', grandeza='ENDERECO',
                                               valor=str(self.idRede))

                        # altera os relacionamentos de grandezas
                        sg = SensorGrandeza.objects.filter(
                            sensor_id=self.original_idRede).all()
                        for x in range(len(sg)):
                            sg[x].sensor_id = self.idRede
                            sg[x].save()

            except Exception as e:
                from central.log import log
                log('MOD03.0', str(e))

    def __str__(self):
        return str(self.descricao) + " [ " + str(self.idRede) + " ]"

    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'


class SensorGrandeza(models.Model):
    obs = models.CharField(max_length=255, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True)
    curvaCalibracao = models.CharField(max_length=255)
    sync = models.BooleanField(default=False, null=False)

    grandeza = models.ForeignKey(
        Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(
        Sensor, to_field='idRede', on_delete=models.PROTECT)

    class Meta:
        # define combinacao unica
        unique_together = ('grandeza', 'sensor')
        verbose_name = 'Grandeza do Sensor'
        verbose_name_plural = 'Grandezas dos Sensores'

    def __str__(self):
        return str(self.sensor.idRede) + " - " + str(self.grandeza)


class Leitura(models.Model):
    valor = models.FloatField()
    createdAt = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False, null=False)

    ambiente = models.ForeignKey(
        Ambiente, to_field='id', on_delete=models.PROTECT, default=0)
    grandeza = models.ForeignKey(
        Grandeza, to_field='codigo', on_delete=models.PROTECT)
    sensor = models.ForeignKey(
        Sensor, to_field='idRede', on_delete=models.PROTECT)

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
    ambiente = models.ForeignKey(
        Ambiente, to_field='id', on_delete=models.PROTECT)
    grandeza = models.ForeignKey(
        Grandeza, to_field='codigo', on_delete=models.PROTECT)

    # sobrescreve o método save para adicionar o valor para o código do alarme
    def save(self, *args, **kwargs):
        if(self.codigoAlarme == None):
            self.codigoAlarme = str(uuid.uuid4())
        # Call the "real" save() method.
        super(AlarmeAnalogico, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Alarme Analógico'
        verbose_name_plural = 'Alarmes Analógicos'

    def __str__(self):
        return str(self.mensagemAlarme) + " [on:" + str(self.valorAlarmeOn) + ", off:" + str(self.valorAlarmeOff) + "]"
