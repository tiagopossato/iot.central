# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 10:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0002_auto_20170802_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarme',
            fields=[
                ('uid', models.CharField(blank=True, max_length=48, null=True)),
                ('codigoAlarme', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Codigo')),
                ('mensagemAlarme', models.CharField(max_length=255)),
                ('prioridadeAlarme', models.IntegerField()),
                ('ativo', models.BooleanField(default=False)),
                ('tempoAtivacao', models.DateTimeField()),
                ('syncAtivacao', models.BooleanField(default=False)),
                ('tempoInativacao', models.DateTimeField(null=True)),
                ('syncInativacao', models.BooleanField(default=False)),
                ('ambiente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Ambiente')),
            ],
            options={
                'verbose_name_plural': 'Alarmes',
                'verbose_name': 'Alarme',
            },
        ),
        migrations.CreateModel(
            name='Grandeza',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('unidade', models.CharField(max_length=15, unique=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('sync', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Grandezas',
                'verbose_name': 'Grandeza',
            },
        ),
        migrations.CreateModel(
            name='Leitura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('sync', models.BooleanField(default=False)),
                ('ambiente', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Ambiente')),
                ('grandeza', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Grandeza')),
            ],
            options={
                'verbose_name_plural': 'Leituras',
                'verbose_name': 'Leitura',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('idRede', models.IntegerField(unique=True, verbose_name='ID de rede')),
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Identificador')),
                ('descricao', models.CharField(default='', max_length=255, unique=True, verbose_name='Descrição')),
                ('intervaloLeitura', models.IntegerField(default=2, verbose_name='Intervalo de leitura')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('sync', models.BooleanField(default=False)),
                ('ambiente', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Ambiente')),
            ],
            options={
                'verbose_name_plural': 'Sensores',
                'verbose_name': 'Sensor',
            },
        ),
        migrations.CreateModel(
            name='SensorGrandeza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obs', models.CharField(blank=True, max_length=255, null=True, verbose_name='Observação')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('curvaCalibracao', models.CharField(max_length=255, verbose_name='Curva de calibração')),
                ('sync', models.BooleanField(default=False)),
                ('grandeza', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Grandeza')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Sensor')),
            ],
            options={
                'verbose_name_plural': 'Grandezas dos Sensores',
                'verbose_name': 'Grandeza do Sensor',
            },
        ),
        migrations.AddField(
            model_name='sensor',
            name='grandezas',
            field=models.ManyToManyField(through='aplicacao.SensorGrandeza', to='aplicacao.Grandeza'),
        ),
        migrations.AddField(
            model_name='leitura',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aplicacao.Sensor', to_field='idRede'),
        ),
        migrations.AlterUniqueTogether(
            name='sensorgrandeza',
            unique_together=set([('grandeza', 'sensor')]),
        ),
    ]
