# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-14 16:09
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tagging.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_name', models.CharField(max_length=200)),
                ('deck_format', models.CharField(choices=[(b'STD', b'Standard'), (b'MDN', b'Modern'), (b'LGC', b'Legacy'), (b'VTG', b'Vintage'), (b'EDH', b'Commander/EDH'), (b'PAU', b'Pauper')], max_length=50)),
                ('deck_price_paper', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('deck_price_online', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('deck_privacy', models.BooleanField()),
                ('deck_need_feedback', models.BooleanField()),
                ('deck_rating', models.IntegerField()),
                ('deck_last_edited', models.DateTimeField()),
                ('deck_tags', tagging.fields.TagField(blank=True, max_length=255)),
                ('deck_description', models.CharField(max_length=5000)),
                ('decklist_mainboard', models.CharField(max_length=500)),
                ('decklist_sideboard', models.CharField(blank=True, max_length=500)),
                ('deck_owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
