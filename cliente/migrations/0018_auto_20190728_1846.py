# Generated by Django 2.1.4 on 2019-07-28 21:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0017_auto_20190502_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='cartaoCredito',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cvv',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='dataValidade',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nomeTitular',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='senhaTemporaria',
            field=models.CharField(max_length=255, null=True, verbose_name='Senha'),
        ),
        migrations.AlterField(
            model_name='controledecliente',
            name='numeroDeVisualizacoesPagas',
            field=models.PositiveIntegerField(blank=True, help_text='Utilize essa opção para acrescentar créditos relacionados ao usuário.', null=True, verbose_name='Créditos de visualização de Oportunidades Pagas'),
        ),
        migrations.AlterField(
            model_name='controledecliente',
            name='terminoDeVigenciaMensal',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 28, 21, 46, 57, 657869, tzinfo=utc), null=True),
        ),
    ]