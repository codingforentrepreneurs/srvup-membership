# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20150206_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermerchantid',
            name='plan_id',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermerchantid',
            name='subscription_id',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 6, 22, 32, 49, 703397, tzinfo=utc), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 6, 22, 32, 49, 703595, tzinfo=utc), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
