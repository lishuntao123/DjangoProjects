# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-11-10 21:27
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20191110_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=models.CharField(max_length=300, verbose_name='课程描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]