# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20150117_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='videos',
            field=models.ManyToManyField(to='videos.Video', null=True, blank=True),
            preserve_default=True,
        ),
    ]
