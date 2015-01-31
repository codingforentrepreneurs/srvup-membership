# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_pageview_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2015, 1, 31, 19, 34, 58, 891630, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
