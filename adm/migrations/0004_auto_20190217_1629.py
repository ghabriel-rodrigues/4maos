# Generated by Django 2.1.4 on 2019-02-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0003_auto_20190216_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='codigoPagSeguro',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='valorCentavos',
            field=models.CharField(default='00', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor',
            field=models.CharField(max_length=6),
        ),
    ]
