# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20150206_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermerchantid',
            name='plan_id',
        ),
        migrations.RemoveField(
            model_name='usermerchantid',
            name='subscription_id',
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 7, 1, 40, 27, 325799, tzinfo=utc), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 7, 1, 40, 27, 326015, tzinfo=utc), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
