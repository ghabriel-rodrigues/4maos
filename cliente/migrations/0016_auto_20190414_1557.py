# Generated by Django 2.1.4 on 2019-04-14 18:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0015_auto_20190414_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controledecliente',
            name='terminoDeVigenciaMensal',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 14, 18, 57, 10, 416917, tzinfo=utc), null=True),
        ),
    ]