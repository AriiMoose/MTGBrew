# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-10 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brew', '0010_auto_20170104_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_privacy',
            field=models.CharField(choices=[(b'PUB', b'Public'), (b'PRV', b'Private'), (b'UNL', b'Unlisted')], max_length=20),
        ),
    ]
