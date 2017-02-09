# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuracoes',
            options={'verbose_name': 'Configuração', 'verbose_name_plural': 'Configurações'},
        ),
        migrations.AddField(
            model_name='configuracoes',
            name='portaSerial',
            field=models.CharField(default='/dev/ttyAMA0', max_length=20),
        ),
        migrations.AddField(
            model_name='configuracoes',
            name='taxa',
            field=models.IntegerField(default=115200),
        ),
    ]
