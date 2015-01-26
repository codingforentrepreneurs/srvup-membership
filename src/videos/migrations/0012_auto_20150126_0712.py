# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'python', b'python'), (b'django', b'django'), (b'css', b'css'), (b'bootstrap', b'bootstrap')]),
            preserve_default=True,
        ),
    ]
