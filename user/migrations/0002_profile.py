# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-23 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('武汉', '武汉'), ('成都', '成都')], default='上海', max_length=10, verbose_name='目标城市')),
                ('dating_gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], default='female', max_length=10, verbose_name='匹配的性别')),
                ('min_distance', models.FloatField(default=1.0, verbose_name='最小查找范围')),
                ('max_distance', models.FloatField(default=10.0, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('vibration', models.BooleanField(default=True, verbose_name='是否开启震动')),
                ('only_matched', models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
        ),
    ]
