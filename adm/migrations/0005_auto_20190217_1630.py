# Generated by Django 2.1.4 on 2019-02-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0004_auto_20190217_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='valor',
            field=models.CharField(max_length=10),
        ),
    ]
