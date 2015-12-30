# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_slug', models.SlugField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('paragraph_hash', models.IntegerField(db_index=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('article_slug', 'paragraph_hash', 'timestamp'),
            },
        ),
    ]
