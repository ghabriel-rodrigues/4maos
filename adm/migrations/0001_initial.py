# Generated by Django 2.1.4 on 2019-02-16 19:12

import adm.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('arquivo', models.FileField(blank=True, null=True, upload_to=adm.models.get_file_path)),
                ('imagem', models.ImageField(null=True, upload_to=adm.models.get_image_path, verbose_name='Imagem')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'verbose_name': 'Arquivo',
                'verbose_name_plural': 'Arquivos',
            },
        ),
        migrations.CreateModel(
            name='ConteudoEducativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descricao', models.TextField()),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conteudo Educativo',
                'verbose_name_plural': 'Conteudo Educativo',
            },
        ),
        migrations.CreateModel(
            name='DuvidasFrequentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.CharField(max_length=500)),
                ('resposta', models.TextField()),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dúvida Frequente',
                'verbose_name_plural': 'Dúvidas Frequentes',
            },
        ),
        migrations.CreateModel(
            name='DuvidasSobreOportunidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('descricao', models.TextField(verbose_name='Resposta')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dúvida',
                'verbose_name_plural': 'Dúvidas',
            },
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=96, null=True, unique=True, verbose_name='Nome')),
                ('videolink', models.CharField(blank=True, max_length=152, null=True, verbose_name='Link video')),
                ('capa', models.ImageField(blank=True, null=True, upload_to=adm.models.get_image_galeria_path, verbose_name='Capa')),
                ('nomeCapa', models.CharField(blank=True, max_length=296, null=True, verbose_name='Título flutuante sobre a capa')),
                ('textCapa', models.CharField(blank=True, max_length=296, null=True, verbose_name='Texto flutuante sobre a capa')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('arquivos', models.ManyToManyField(blank=True, related_name='galeria_arquivos', to='adm.Arquivo', verbose_name='Arquivos')),
            ],
            options={
                'verbose_name': 'Galeria',
                'verbose_name_plural': 'Galerias',
            },
        ),
        migrations.CreateModel(
            name='LinksDoMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Links do Menu',
                'verbose_name_plural': 'Links do Menu',
            },
        ),
        migrations.CreateModel(
            name='MaterialDeApoioBasico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Material de Apoio Básico',
                'verbose_name_plural': 'Materiais de Apoio Básico',
            },
        ),
        migrations.CreateModel(
            name='MaterialDeMarketingAvancado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Material de Marketing Avançado',
                'verbose_name_plural': 'Materiais de Marketing Avançado',
            },
        ),
        migrations.CreateModel(
            name='Necessidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('assunto', models.CharField(max_length=300)),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('mensagem', models.TextField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Necessidade',
                'verbose_name_plural': 'Necessidades',
            },
        ),
        migrations.CreateModel(
            name='Oportunidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoDeOportunidade', models.CharField(choices=[('paga', 'Paga'), ('disfarcada', 'Disfarçada')], max_length=30, verbose_name='Tipo de oportunidade')),
                ('status', models.CharField(choices=[('Aguardando publicação', 'Aguardando publicação'), ('Tentando contato', 'Tentando contato'), ('Em andamento', 'Em andamento'), ('Finalizado', 'Finalizado')], max_length=30)),
                ('primeiroNome', models.CharField(blank=True, help_text='Primeiro nome do responsável pela oportunidade', max_length=300, null=True, verbose_name='Primeiro nome')),
                ('nomeCompleto', models.CharField(blank=True, max_length=600, null=True, verbose_name='Nome completo')),
                ('nome', models.CharField(max_length=300, verbose_name='Título da oportunidade')),
                ('empresa', models.CharField(blank=True, max_length=500, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True, verbose_name='CNPJ')),
                ('telefone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('bairro', models.CharField(blank=True, max_length=300, null=True)),
                ('endereco', models.CharField(blank=True, max_length=600, null=True, verbose_name='Endereço')),
                ('preferencia', models.CharField(blank=True, choices=[('Melhor qualidade', 'Melhor qualidade'), ('Menor preco', 'Menor preço'), ('Custo / beneficios', 'Custo / Benefícios')], max_length=300, null=True, verbose_name='Preferência')),
                ('grauDeUrgencia', models.CharField(blank=True, choices=[('Imediata', 'Imediata'), ('Em breve', 'Em breve'), ('Apenas uma pesquisa', 'Em breve')], max_length=300, null=True, verbose_name='Grau de Urgência')),
                ('numeroDeParticipantes', models.IntegerField(blank=True, null=True, verbose_name='Número de participantes')),
                ('quantidadeDeFuncionarios', models.IntegerField(blank=True, null=True, verbose_name='Qnt de funcionários')),
                ('cidade', models.CharField(choices=[('BH', 'Belo Horizonte - MG'), ('SP', 'São Paulo - SP')], max_length=30)),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('dataDeSolicitacao', models.DateTimeField(blank=True, null=True, verbose_name='Data de solicitação')),
                ('dataDeFinalizacao', models.DateTimeField(blank=True, null=True, verbose_name='Data de finalização')),
                ('dataDePublicacao', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Data de publicação')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Data de cadastro')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Inativo', 'Inativo'), ('Ativo', 'Ativo')], max_length=30)),
                ('nome', models.CharField(max_length=300)),
                ('periodicidadeDosServicosGratuitos', models.PositiveIntegerField(blank=True, help_text='Informe em meses a disponibilidade dos serviços gratuitos', null=True, verbose_name='Periodicidade em meses')),
                ('numeroDeVezesDeAcessibilidadeGratuita', models.PositiveIntegerField(default=1, help_text='Informe o número de vezes de acessibilidade dos serviços gratuitos', verbose_name='Acessibilidade gratuita')),
                ('quantidadePadraoDeOportunidadesPagas', models.PositiveIntegerField(default=1, verbose_name='Quantidade de oportunidades pagas')),
                ('quantidadePadraoDeOportunidadesDisfarcadas', models.PositiveIntegerField(default=3, verbose_name='Quantidade de oportunidades disfarçadas')),
                ('mesesParaExpirar', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero de meses de vigência')),
                ('diasParaExpirar', models.PositiveIntegerField(blank=True, null=True, verbose_name='Dias para expirar')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('linksAcessiveis', models.ManyToManyField(blank=True, related_name='plano_links', to='adm.LinksDoMenu', verbose_name='Links acessiveis pelo plano')),
            ],
            options={
                'verbose_name': 'Plano',
                'verbose_name_plural': 'Planos',
            },
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('descricao', models.TextField(blank=True, default='', null=True)),
                ('valor', models.CharField(max_length=10)),
                ('link', models.SlugField(help_text="URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.", null=True, unique=True, verbose_name='URL amigavel')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to=adm.models.get_serv_path, verbose_name='Imagem')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('galeria', models.ManyToManyField(blank=True, related_name='servico_galeria', to='adm.Galeria', verbose_name='Galeria de arquivos')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TratativasDeOportunidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Tentando contato', 'Tentando contato'), ('Primeiro contato realizado', 'Primeiro contato realizado'), ('Proposta enviada', 'Proposta enviada'), ('Aguardando retorno do cliente', 'Aguardando retorno do cliente'), ('Proposta aprovada', 'Proposta aprovada'), ('Proposta rejeitada', 'Proposta rejeitada')], max_length=30)),
                ('dataDoProximoContato', models.DateField(blank=True, null=True, verbose_name='Data do próximo contato')),
                ('dataDeCadastro', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('justificativa', models.TextField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('oportunidadeRelacionada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.Oportunidade')),
            ],
            options={
                'verbose_name': 'Tratativa',
                'verbose_name_plural': 'Tratativas',
            },
        ),
        migrations.AddField(
            model_name='plano',
            name='servicosGratuitos',
            field=models.ManyToManyField(blank=True, related_name='plano_links', to='adm.Servico', verbose_name='Serviços gratuitos do plano'),
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='servicoSolicitado',
            field=models.ManyToManyField(blank=True, related_name='oportunidade_servico', to='adm.Servico', verbose_name='Serviço Pretendido'),
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='tipoDeCliente',
            field=models.ManyToManyField(blank=True, related_name='oportunidade_tipodecliente', to='adm.TipoDeCliente', verbose_name='Tipo de cliente'),
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='tipoDeEmpresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.TipoDeEmpresa', verbose_name='Tipo de Empresa'),
        ),
        migrations.AddField(
            model_name='materialdemarketingavancado',
            name='servicos',
            field=models.ManyToManyField(blank=True, related_name='materialavancado_servicos', to='adm.Servico', verbose_name='Serviços'),
        ),
        migrations.AddField(
            model_name='materialdeapoiobasico',
            name='servicos',
            field=models.ManyToManyField(blank=True, related_name='materialapoio_servicos', to='adm.Servico', verbose_name='Serviços'),
        ),
        migrations.AddField(
            model_name='duvidassobreoportunidades',
            name='oportunidadeRelacionada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.Oportunidade'),
        ),
        migrations.AddField(
            model_name='conteudoeducativo',
            name='galeria',
            field=models.ManyToManyField(blank=True, related_name='conteudoeducativo_galeria', to='adm.Galeria', verbose_name='Galeria de arquivos'),
        ),
    ]