# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0015_auto_20150207_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 7, 2, 6, 28, 708564, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
