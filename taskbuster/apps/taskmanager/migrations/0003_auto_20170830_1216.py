# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0002_auto_20170830_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('user', models.ForeignKey(related_name='tags', verbose_name='user', to='taskmanager.Profile')),
            ],
            options={
                'ordering': ('user', 'name'),
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('user', 'name')]),
        ),
    ]
