# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20150117_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='videos',
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(to='videos.Category', null=True),
            preserve_default=True,
        ),
    ]
