# Generated by Django 2.1.4 on 2019-02-16 20:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controledecliente',
            options={'verbose_name': 'Controle', 'verbose_name_plural': 'Controle de clientes'},
        ),
        migrations.AlterModelOptions(
            name='negociacoesdeoportunidades',
            options={'verbose_name': 'Negociação', 'verbose_name_plural': 'Negociações de oportunidades'},
        ),
        migrations.AlterField(
            model_name='cliente',
            name='status',
            field=models.CharField(blank=True, choices=[('Inativo', 'Inativo'), ('Inativo - Cancelado', 'Inativo - Cancelado'), ('Ativo', 'Ativo'), ('Ativo - Cadastro incompleto', 'Ativo - Cadastro incompleto'), ('Ativo - Pagamento pendente', 'Ativo - Pagamento pendente')], default='Inativo', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='controledecliente',
            name='terminoDeVigenciaMensal',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 16, 20, 32, 51, 573654, tzinfo=utc), null=True),
        ),
    ]
