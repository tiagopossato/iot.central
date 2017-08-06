from django.db import models
from os.path import abspath
from os import remove
import os
import errno

class Mqtt(models.Model):
    STATUS = (
        (0, 'Não configurado'),
        (1, 'Funcionando'),
        (2, 'Falha na comunicação'),
        (3, 'Erro'),
    )
    id = models.AutoField(primary_key=True)
    identificador = models.UUIDField("Identificador", default='')
    status = models.IntegerField(
        'Estado da comunicação', default=0, choices=STATUS)
    descricao = models.CharField(
        'Descrição', null=True, blank=True, max_length=255)
    servidor = models.CharField(
        'Endereço do servidor', null=True, blank=True, max_length=255)
    keyFile = models.FilePathField('Chave privada', null=True, blank=True)
    certFile = models.FilePathField('Chave pública', null=True, blank=True)
    caFile = models.FilePathField('Certificado de autoridade', null=True, blank=True)

    class Meta:
        verbose_name = 'Configurações da comunicação MQTT'

    def save(self, trocarCertificados = False, *args, **kwargs):
        """
        Método sobrescrito para criar o certificado antes de salvar
        """
        try:
            if(trocarCertificados):
                print("Trocando certificados")
                # Salva os certificados no HD e troca
                f = open('certs/keyFile.key', 'w')
                f.write(self.keyFile)
                self.keyFile = abspath(f.name)

                f = open('certs/certFile.crt', 'w')
                f.write(self.certFile)
                self.certFile = abspath(f.name)

                f = open('certs/ca.crt', 'w')
                f.write(self.caFile)
                self.caFile = abspath(f.name)

            super(Mqtt, self).save(*args, **kwargs)
        except Exception as e:
            print(str(e))

    def delete(self, *args, **kwargs):
        try:
            # Apaga os certificados no hd
            # remove(self.certFile)
            # remove(self.keyFile)
            # remove(self.caFile)
            super(Mqtt, self).delete(*args, **kwargs)
        except Exception as e:
            print(str(e))
