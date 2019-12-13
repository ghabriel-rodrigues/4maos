from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid
import os


def get_image_path(instance, filename):
    return os.path.join('imgs', "img_id_%s" % str(uuid.uuid4().hex), filename)

def get_image_galeria_path(instance, filename):
    return os.path.join('capas', "galeria_id_%s" % str(uuid.uuid4().hex), filename)

def get_file_path(instance, filename):
    return os.path.join('arquivos', "arquivo_id_%s" % str(uuid.uuid4().hex), filename)

def get_serv_path(instance, filename):
    return os.path.join('servicos', "servico_id_%s" % str(uuid.uuid4().hex), filename)

class TipoDeCliente(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=300)

    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.nome

class TipoDeEmpresa(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=300)

    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.nome

class Arquivo(models.Model):
    choices_coordenadas = (
        ('Canto superior direito', 'Canto superior direito'),
        ('Canto superior esquerdo', 'Canto superior esquerdo'),
        ('Canto inferior direito', 'Canto inferior direito'),
        ('Canto inferior esquerdo', 'Canto inferior esquerdo'),
        ('Centro', 'Centro')
    )

    nome = models.CharField(max_length=300)
    arquivo = models.FileField(upload_to=get_file_path, blank=True, null = True)
    choices_coordenadas = models.CharField("Coordenadas", blank=True, null = True, max_length=30, choices=choices_coordenadas, help_text="Escolha a coordenada que ficará a logo do cliente nessa arte, caso esse arquivo corresponda ao post de artes para cliente.")
    
    imagem = models.ImageField(u"Imagem", upload_to=get_image_path, blank = False, null = True)
    
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null = True)

    def __str__(self):
        return self.nome

    def get_absolute_file_url(self):
        if settings.ONLINE:
            return settings.MEDIA_URL+"%s/" % self.arquivo
        else:
            return "http://localhost:8000/media/arquivos"+"%s/" % self.arquivo

    def get_absolute_img_url(self):
        return settings.MEDIA_URL+"%s/" % self.imagem


    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

class Galeria(models.Model) :
    nome = models.CharField("Nome", max_length = 96, unique = True, blank = False, null = True)
    videolink = models.CharField("Link video", max_length = 152, blank = True, null = True)
    capa = models.ImageField(u"Capa", upload_to=get_image_galeria_path, blank = True, null = True)
    nomeCapa = models.CharField("Título flutuante sobre a capa", max_length = 296, blank = True, null = True)
    textCapa = models.CharField("Texto flutuante sobre a capa", max_length = 296, blank = True, null = True)

    arquivos = models.ManyToManyField('Arquivo', related_name="galeria_arquivos",
        verbose_name = "Arquivos", blank = True)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null = True)

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerias"

    def __str__(self) :
        return self.nome

class Videos(models.Model) :
    nome = models.CharField("Nome", max_length = 255, unique = True, blank = False, null = True)
    urlYoutube = models.CharField("Url do video", max_length=150, blank=True, null=True,help_text = u"Insira a URL de incorporação do video. Não esqueça do http://. Exemplo: http://www.youtube.com/embed/C_NPf7dWP7g")
    assunto = models.CharField("Assunto", max_length = 255, blank = True, null = True)

    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null = True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self) :
        return self.nome

    def getVideo(self):
        return "%s" % self.urlYoutube

class LivrosArtigos(models.Model) :
    nome = models.CharField("Nome", max_length = 96, unique = True, blank = False, null = True)
    autor = models.CharField("Autor", max_length = 152, blank = True, null = True)
    sinopse = models.CharField("Sinopse", max_length = 152, blank = True, null = True)
    capa = models.ImageField(u"Capa", upload_to=get_image_galeria_path, blank = True, null = True)

    arquivo = models.ForeignKey('Arquivo', on_delete=models.DO_NOTHING, blank = False, null = False)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null = True)

    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

    def __str__(self) :
        return self.nome

class Blog(models.Model) :
    nome = models.CharField("Nome", max_length = 96, unique = True, blank = False, null = True)
    sinopse = models.CharField("Sinopse", max_length = 152, blank = True, null = True)
    conteudo = models.TextField(default="", null=True, blank=True)
    arquivo = models.ForeignKey('Arquivo', on_delete=models.DO_NOTHING, blank = True, null = True)

    capa = models.ImageField(u"Capa", upload_to=get_image_galeria_path, blank = True, null = True)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null = True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Blog"

    def __str__(self) :
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=400)
    descricao = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Servico(models.Model):
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome = models.CharField(max_length=255, unique=True)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(default="", null=True, blank=True)
    codigoPagSeguro = models.TextField(default="", null=True, blank=True)
    valor = models.CharField(max_length=10, null=True, blank=True)
    link = models.SlugField(verbose_name="URL amigavel", unique = True, blank = False, null = True, help_text = u"URLs devem ser compostos apenas de letras minusculas, '_' , '-' e numeros.")
    imagem = models.ImageField(u"Imagem", upload_to = get_serv_path, blank = True, null = True)
    galeria = models.ManyToManyField('Galeria', related_name="servico_galeria",
        verbose_name = "Galeria de arquivos", blank = True)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)
    visualizar = models.BooleanField(help_text="Este serviço deve ter o botão de visualizar?", default=False)

    def __str__(self):
        return self.nome

    def get_absolute_url(self) :
        return "/servico/%s/" % self.link

class ListaDeServicosDoFiltroDeOportunidades(models.Model):
    servicosFiltraveis = models.ManyToManyField('Servico', related_name="lista_servico",
        verbose_name="Serviços Filtráveis", blank = True, help_text="Por favor, selecione os serviços que farão parte do filtro de oportunidades.")

    class Meta:
        verbose_name = "Lista de serviços do filtro de oportunidades"
        verbose_name_plural = "Lista de serviços"

    def __str__(self):
        return "Listagem"

class Cidade(models.Model):
    nome = models.CharField(max_length=400)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

class Oportunidade(models.Model):
    choices_tipoOportunidade = (
        ('paga', 'Paga'),
        ('disfarcada', 'Disfarçada'),
    )
    choices_status = (
        ('Aguardando publicação', 'Aguardando publicação'),
        ('Tentando contato', 'Tentando contato'),
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
    )
    choices_grauDeUrgencia = (
        ('Imediata', 'Imediata'),
        ('Em breve', 'Em breve'),
        ('Apenas uma pesquisa', 'Apenas uma pesquisa'),
    )
    choices_PREFERENCIA = (
        ('Melhor qualidade', 'Melhor qualidade'),
        ('Menor preço', 'Menor preço'),
        ('Custo / Benefícios', 'Custo / Benefícios'),
    )
    tipoDeOportunidade = models.CharField("Tipo de oportunidade", max_length=30, choices=choices_tipoOportunidade)
    status = models.CharField(max_length=30, choices=choices_status)

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    primeiroNome = models.CharField('Primeiro nome', help_text="Primeiro nome do responsável pela oportunidade", max_length=300, blank=True, null=True)
    nomeCompleto = models.CharField('Nome completo', max_length=600, blank=True, null=True)
    nome = models.CharField(verbose_name="Título da oportunidade", max_length=300)
    empresa = models.CharField(max_length=500, blank=True, null=True)
    tipoDeEmpresa = models.ForeignKey(TipoDeEmpresa, blank=True, null=True, verbose_name="Tipo de Empresa", on_delete=models.CASCADE)

    cnpj = models.CharField(verbose_name="CNPJ",max_length=14, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    endereco = models.CharField("Endereço", max_length=600, blank=True, null=True)
    bairro = models.CharField(max_length=300, blank=True, null=True)
    cidade =  models.ForeignKey(Cidade, on_delete=models.DO_NOTHING, blank=True, null=True)

    preferencia = models.CharField("Preferência", choices=choices_PREFERENCIA, max_length=300, blank=True, null=True)
    grauDeUrgencia = models.CharField("Grau de Urgência", choices=choices_grauDeUrgencia, max_length=300, blank=True, null=True)
    numeroDeParticipantes = models.PositiveIntegerField("Número de participantes", blank=False, null=True)

    servicoSolicitado = models.ManyToManyField('Servico', related_name="oportunidade_servico",
        verbose_name="Serviço Pretendido", blank = True)
    tipoDeCliente = models.ManyToManyField('TipoDeCliente', related_name="oportunidade_tipodecliente",
        verbose_name="Tipo de cliente", blank = True)

    observacoes = models.TextField("Observações", blank=True, null=True)

    dataDeSolicitacao = models.DateTimeField("Data de solicitação", blank=True, null=True)
    dataDeFinalizacao = models.DateTimeField("Data de finalização", blank=True, null=True)
    dataDePublicacao = models.DateTimeField("Data de publicação", default=timezone.now, blank=True, null=True)
    dataDeCadastro = models.DateTimeField("Data de cadastro", default=timezone.now, blank=True, null=True)

    def publicar(self):
        self.dataDePublicacao = timezone.now()
        self.save()

    def getTotalParticipantes(self):
        return self.negociacoesdeoportunidades_set.all().count()

    def temDuvidas(self):
        if self.duvidassobreoportunidades_set.all().count() > 0:
            return True
        return False

    def isTotalMenorQueNumero(self): #total de participantes é menor que o numero de participantes?
        if self.negociacoesdeoportunidades_set.all().count() < self.numeroDeParticipantes:
            return True
        return False

    def isTotalMenorQueNumeroView(self): #total de participantes é menor que o numero de participantes?
        if self.negociacoesdeoportunidades_set.all().count() <= self.numeroDeParticipantes:
            return True
        return False

    def __str__(self):
        return self.nome

class TratativasDeOportunidades(models.Model):
    choices_status = (
        ('Tentando contato', 'Tentando contato'),
        ('Primeiro contato realizado', 'Primeiro contato realizado'),
        ('Proposta enviada', 'Proposta enviada'),
        ('Aguardando retorno do cliente', 'Aguardando retorno do cliente'),
        ('Proposta aprovada', 'Proposta aprovada'),
        ('Proposta rejeitada', 'Proposta rejeitada'),
    )
    status = models.CharField(max_length=30, choices=choices_status)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    oportunidadeRelacionada = models.ForeignKey('Oportunidade', on_delete=models.CASCADE)

    dataDoProximoContato = models.DateField(verbose_name="Data do próximo contato", blank=True, null=True)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)
    justificativa = models.TextField()

    class Meta:
        verbose_name = "Tratativa"
        verbose_name_plural = "Tratativas"


    def __str__(self):
        return self.oportunidadeRelacionada.nome

class DuvidasSobreOportunidades(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    oportunidadeRelacionada = models.ForeignKey('Oportunidade', on_delete=models.CASCADE)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)
    descricao = models.TextField(verbose_name="Resposta")

    def __str__(self):
        return self.oportunidadeRelacionada.nome

    class Meta:
        verbose_name = "Dúvida"
        verbose_name_plural = "Dúvidas"

class Necessidades(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nome = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=20)
    assunto = models.CharField(max_length=300)
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)
    mensagem = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Necessidade"
        verbose_name_plural = "Necessidades"

class DuvidasFrequentes(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    pergunta = models.CharField(max_length=500)
    resposta = models.TextField()
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.pergunta

    class Meta:
        verbose_name = "Dúvida Frequente"
        verbose_name_plural = "Dúvidas Frequentes"

class ConteudoEducativo(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    videos = models.ManyToManyField('Videos', related_name="conteudoeducativo_videos",
        verbose_name = "Vídeos", blank = True)
    blog = models.ManyToManyField('Blog', related_name="conteudoeducativo_blog",
        verbose_name = "Blog", blank = True)
    livros = models.ManyToManyField('LivrosArtigos', related_name="conteudoeducativo_livros",
        verbose_name = "Ebooks", blank = True)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Conteudo Educativo"
        verbose_name_plural = "Conteudo Educativo"

class MaterialDeMarketingAvancado(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    servicos = models.ManyToManyField('Servico', related_name="materialavancado_servicos",
        verbose_name = "Serviços", blank = True)
    titulo = models.CharField(max_length=300)
    descricao = models.TextField(verbose_name="Descrição")
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Material de Marketing Avançado"
        verbose_name_plural = "Materiais de Marketing Avançado"

class MaterialDeApoioBasico(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    servicos = models.ManyToManyField('Servico', related_name="materialapoio_servicos",
        verbose_name = "Serviços", blank = True)
    titulo = models.CharField(max_length=300)
    descricao = models.TextField(verbose_name="Descrição")
    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Material de Apoio Básico"
        verbose_name_plural = "Materiais de Apoio Básico"

class LinksDoMenu(models.Model):
    choices_links = (
        ('oportunidades', 'oportunidades'),
        ('oportunidades-disfarcadas', 'oportunidades-disfarcadas'),
        ('duvidas-frequentes', 'duvidas-frequentes'),
        ('conteudo-educativo', 'conteudo-educativo'),
        ('material-marketing-apoio', 'material-marketing-apoio'),
        ('material-marketing-avancado', 'material-marketing-avancado'),
        ('perfil', 'perfil'),
        ('planos', 'planos'),
    )

    nome = models.CharField(max_length=200)
    link = models.CharField(max_length=500, choices = choices_links)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Links do Menu"
        verbose_name_plural = "Links do Menu"

class Plano(models.Model):
    choices_status = (
        ('Inativo', 'Inativo'),
        ('Ativo', 'Ativo')
    )
    status = models.CharField(max_length=30, choices=choices_status)
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=300)
    linksAcessiveis = models.ManyToManyField('LinksDoMenu', related_name="plano_links",
        verbose_name = "Links acessiveis pelo plano", blank = True)
    servicosGratuitos = models.ManyToManyField('Servico', related_name="plano_links",
        verbose_name = "Serviços gratuitos do plano", blank = True)
    periodicidadeDosServicosGratuitos = models.PositiveIntegerField(
        verbose_name="Periodicidade em meses", help_text="Informe em meses a disponibilidade dos serviços gratuitos",
        blank=True, null=True)
    numeroDeVezesDeAcessibilidadeGratuita = models.PositiveIntegerField(
        verbose_name="Acessibilidade gratuita", help_text="Informe o número de vezes de acessibilidade dos serviços gratuitos",
        blank=False, null=False, default=1)
    quantidadePadraoDeOportunidadesPagas = models.PositiveIntegerField(
        verbose_name="Quantidade de oportunidades pagas",
        blank=False, null=False, default=1)
    # quantidadePadraoDeOportunidadesDisfarcadas = models.PositiveIntegerField(
    #     verbose_name="Quantidade de oportunidades disfarçadas",
    #     blank=True, null=True, default=0)
    mesesParaExpirar = models.PositiveIntegerField(
        verbose_name="Numero de meses de vigência",
        blank=False, null=True)
    diasParaExpirar = models.PositiveIntegerField(
        verbose_name="Dias para expirar",
        blank=False, null=True)

    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"

    def __str__(self):
        return self.nome

    def hasLinkMaterialAvancado(self):
        for item in self.linksAcessiveis.all():
            if item.link == "material-marketing-avancado":
                return True
        return False
    def hasLinkMaterialBasico(self):
        for item in self.linksAcessiveis.all():
            if item.link == "material-marketing-apoio":
                return True
        return False
    def hasLinkConteudoEducativo(self):
        for item in self.linksAcessiveis.all():
            if item.link == "conteudo-educativo":
                return True
        return False
    def hasLinkDuvidasFrequentes(self):
        for item in self.linksAcessiveis.all():
            if item.link == "duvidas-frequentes":
                return True
        return False
    def hasLinkOportunidadesDisfarcadas(self):
        for item in self.linksAcessiveis.all():
            if item.link == "oportunidades-disfarcadas":
                return True
        return False
    def hasLinkOportunidades(self):
        for item in self.linksAcessiveis.all():
            if item.link == "oportunidades":
                return True
        return False
    def hasLinkPerfil(self):
        for item in self.linksAcessiveis.all():
            if item.link == "perfil":
                return True
        return False
    def hasLinkPlanos(self):
        for item in self.linksAcessiveis.all():
            if item.link == "planos":
                return True
        return False
