# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-01-22 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('haproxy', '0006_auto_20190122_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='backend',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='haproxy.Backend'),
        ),
        migrations.AlterField(
            model_name='option',
            name='frontend',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='haproxy.Frontend'),
        ),
    ]
