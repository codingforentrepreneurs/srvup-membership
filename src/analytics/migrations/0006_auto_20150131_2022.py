# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_auto_20150131_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 31, 20, 22, 18, 666845, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
