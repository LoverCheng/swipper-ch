# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='权限名称')),
                ('description', models.CharField(max_length=300, verbose_name='权限描述')),
            ],
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='会员名称')),
                ('level', models.IntegerField(verbose_name='会员等级')),
                ('duration', models.IntegerField(verbose_name='会员时长')),
                ('price', models.FloatField(verbose_name='会员价格')),
            ],
        ),
        migrations.CreateModel(
            name='VipPermRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_level', models.IntegerField(verbose_name='会员等级')),
                ('perm_id', models.IntegerField(verbose_name='权限 ID')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vippermrelation',
            unique_together=set([('vip_level', 'perm_id')]),
        ),
    ]
