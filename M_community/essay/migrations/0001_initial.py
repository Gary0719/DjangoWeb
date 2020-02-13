# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-16 23:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('classify', models.CharField(max_length=1, verbose_name='话题')),
                ('content', models.CharField(max_length=500, verbose_name='描述')),
                ('image', models.ImageField(upload_to='', verbose_name='附图')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True)),
                ('click_rate', models.IntegerField(default=0, verbose_name='点击率')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='作者')),
            ],
            options={
                'verbose_name': '随笔',
                'verbose_name_plural': '随笔',
                'db_table': 'essay',
            },
        ),
    ]
