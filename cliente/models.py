from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from adm.models import Oportunidade, Plano, Servico
from dateutil.relativedelta import *
from datetime import datetime
import calendar
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
import uuid
import os


def get_logo_path(instance, filename):
    return os.path.join('imgs', "img_id_%s" % str(uuid.uuid4().hex), filename)

class AreaDeAtuacao(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=300)

    dataDeCadastro = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Área de atuação"
        verbose_name_plural = "Áreas de atuação"

class Cliente(models.Model):
    choices_status = (
        ('Inativo', 'Inativo'),
        ('Inativo - Cancelado', 'Inativo - Cancelado'),
        ('Ativo', 'Ativo'),
        ('Ativo - Cadastro incompleto', 'Ativo - Cadastro incompleto'),
        ('Ativo - Pagamento pendente', 'Ativo - Pagamento pendente'),
    )
    choices_tipoDeEscritorio = (
        ('Empresa', 'Empresa'),
        ('Autônomo', 'Autônomo'),
    )


    #  (Abertura de empresas, área Contábil, Gestão Societária,
    #   Assessoria trabalhista, área fiscal,  assessoria tributária,
    #   assessoria empresarial, assessoria financeira,
    #   imposto de renda pessoas física, certificado digital, BPO,
    #   Controle patrimonial, planejamento tributário).

    status = models.CharField(max_length=30, blank = True, null = True, choices=choices_status, default="Inativo")
    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    senhaTemporaria = models.CharField("Senha", max_length = 255, blank = False, null = True, help_text = "")
    email = models.EmailField("Email", blank = False, null = True, help_text = "", unique = True)
    nome = models.CharField("Nome", max_length = 255, blank = False, null = True, help_text = "")
    sobrenome = models.CharField("Sobrenome", max_length = 255, blank = True, null = True, help_text = "")
    cpf = models.CharField("CPF", max_length = 15, blank = True, null = True, help_text = "", unique=True)
    
    cargo = models.CharField("Cargo", max_length = 255, blank = True, null = True, help_text = "")
    departamento = models.CharField("Departamento", max_length = 255, blank = True, null = True, help_text = "")
    rg = models.CharField("RG", max_length = 30, blank = True, null = True, help_text = "", unique=True)
    cnpj = models.CharField("CNPJ", max_length = 30, blank = True, null = True, help_text = "", unique=True)
    razaoSocial = models.CharField("Razão Social / Empresa", max_length = 500, blank = True, null = True, help_text = "")
    nomeDoResponsavel =  models.CharField("Nome do contador responsável pela empresa", max_length = 500, blank = True, null = True, help_text = "")
    crcDoResponsavel =  models.CharField("CRC do contador responsável pela empresa", max_length = 500, blank = True, null = True, help_text = "")
    cpfDoResponsavel = models.CharField("CPF do contador responsável pela empresa", max_length = 15, blank = True, null = True, help_text = "", unique=True)
    tipoDeEscritorio = models.CharField(max_length=30, blank = True, null = True, choices=choices_tipoDeEscritorio, default="Empresa")

    areaDeAtuacao = models.ManyToManyField('AreaDeAtuacao', related_name="cliente_areadeatuacao",
            verbose_name="Área de atuação", blank = True, help_text="Selecione as áreas de atuação de sua empresa")
    cep = models.CharField("CEP", max_length = 10, blank = True, null = True, help_text = "")
    rua = models.CharField("Rua", max_length = 500, blank = True, null = True, help_text = "")
    numero = models.CharField("Numero", max_length = 10, blank = True, null = True, help_text = "")
    bairro = models.CharField("Bairro", max_length = 300, blank = True, null = True, help_text = "")
    cidade = models.CharField("Cidade", max_length = 300, blank = True, null = True, help_text = "")
    telefone = models.CharField("Telefone", max_length = 20, blank = True, null = True, help_text = "")
    
    #cartaoCredito = models.CharField("Cartao de crédito", max_length = 30, blank = True, null = True, help_text = "")
    #nomeTitular = models.CharField("Nome do titular", max_length = 500, blank = True, null = True, help_text = "")
    #dataValidade = models.DateField("Data da validade", blank = True, null = True, help_text = "")
    #cvv = models.CharField("CVV", max_length = 5, blank = True, null = True, help_text = "")
    logo = models.ImageField(u"Logo", upload_to=get_logo_path, blank = True, null = True)
    
    plano = models.ForeignKey(Plano, on_delete=models.DO_NOTHING)
    dataDeCadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
    
    def get_absolute_logo_url(self):
      return settings.MEDIA_URL+"%s/" % self.logo

class ControleDeCliente(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dataDeCadastro = models.DateTimeField(default=timezone.now)
    inicioDeVigenciaDoPlano = models.DateTimeField(default=timezone.now, blank = True, null = True,) #dataDeCadastro + plano.mesesParaExpirar ou diasParaExpirar
    terminoDeVigenciaDoPlano = models.DateTimeField(blank = True, null = True,) #dataDeCadastro + plano.mesesParaExpirar ou diasParaExpirar
    inicioDeVigenciaMensal =  models.DateTimeField(default=timezone.now, blank = True, null = True,) #dataDeCadastro + 1 mes ou diasParaExpirar
    terminoDeVigenciaMensal =  models.DateTimeField(default= timezone.now()+relativedelta(months=+1), blank = True, null = True,) #dataDeCadastro + 1 mes ou diasParaExpirar
    oportunidadesPagasVisualizadasMensais = models.ManyToManyField(Oportunidade, related_name="log_oportunidadespagas",
        verbose_name = "Pagas", help_text="Oportunidades pagas visualizadas mensalmente.", blank = True)
    numeroDeVisualizacoesPagas = models.PositiveIntegerField(verbose_name = "Créditos de visualização de Oportunidades Pagas", null=True, blank= True, help_text="Utilize essa opção para acrescentar créditos relacionados ao usuário.")
    oportunidadesDisfarcadasVisualizadasMensais = models.ManyToManyField(Oportunidade, related_name="log_oportunidadesdisfarcadas",
        verbose_name = "Disfarçadas", help_text="Oportunidades disfarçadas visualizadas mensalmente.", blank = True)
    numeroDeVisualizacoesDisfarcadas = models.PositiveIntegerField(null=True, blank= True)
    servicosSolicitadosMensalmente = models.ManyToManyField(Servico, related_name="log_servicos",
        verbose_name = "Serviços", help_text="Serviços solicitados mensalmente.", blank = True)
    numeroDeServicosSolicitados = models.PositiveIntegerField(null=True, blank= True)

    def __str__(self):
        return self.cliente.nome

    def diasParaPlanoExpirar(self):
        diff = self.terminoDeVigenciaDoPlano - datetime.now(timezone.utc)
        return diff.days

    def checarSeAcabouPlano(self):
        if self.terminoDeVigenciaDoPlano <= datetime.now(timezone.utc):
            return True
        return False

    def checarSeAcabouVigenciaMensal(self):
        if self.terminoDeVigenciaMensal <= datetime.now(timezone.utc):
            return True
        return False

    #corrigir contadores
    def getTotalOportunidades(self):
        return self.numeroDeVisualizacoesPagas + self.numeroDeVisualizacoesDisfarcadas

    def decrementarNumeroDeVisualizacoesPagas(self):
        if(self.numeroDeVisualizacoesPagas >0):
            self.numeroDeVisualizacoesPagas = self.numeroDeVisualizacoesPagas - 1
        return self.numeroDeVisualizacoesPagas

    def decrementarNumeroDeVisualizacoesDisfarcadas(self):
        if(self.numeroDeVisualizacoesDisfarcadas >0):
            self.numeroDeVisualizacoesDisfarcadas = self.numeroDeVisualizacoesDisfarcadas - 1
        return self.numeroDeVisualizacoesDisfarcadas

    def decrementarNumeroDeServicosSolicitados(self):
        self.numeroDeServicosSolicitados = self.numeroDeServicosSolicitados - 1
        return self.numeroDeServicosSolicitados

    def autorizaComunicacaoPagas(self) :
        if self.terminoDeVigenciaDoPlano.utcnow() <= datetime.utcnow():
            if self.numeroDeVisualizacoesPagas > 0:
                if self.numeroDeVisualizacoesPagas <= self.plano.quantidadePadraoDeOportunidadesPagas:

                    return 1 #True
                else:
                    return 2 #False
            else:
                return 3 #False
        else:
            return 4 #False

    # def autorizaComunicacaoDisfarcadas(self) :
    #     if self.terminoDeVigenciaDoPlano.utcnow() <= datetime.utcnow():
    #         if self.numeroDeVisualizacoesDisfarcadas > 0:
    #             if self.numeroDeVisualizacoesDisfarcadas <= self.plano.quantidadePadraoDeOportunidadesDisfarcadas:
    #                 return 1 #True
    #             else:
    #                 return 2 #False
    #         else:
    #             return 3 #False
    #     else:
    #         return 4 #False

    class Meta:
        verbose_name = "Controle"
        verbose_name_plural = "Controle de clientes"

class NegociacoesDeOportunidades(models.Model):
    choices_status = (
        ('Aguardando posicionamento', 'Aguardando posicionamento'),
        ('Acordo feito', 'Acordo feito'),
        ('Encerrada', 'Encerrada'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE)
    controleDeCliente = models.ForeignKey(ControleDeCliente, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=choices_status)
    dataDeCadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s" % (self.oportunidade.nome,self.cliente.nome)

    class Meta:
        verbose_name = "Negociação"
        verbose_name_plural = "Negociações de oportunidades"

    #solicitacao de servico - data, serviço soilicitado
    #se opPagasVis.countSelected > self.plano.quantidadePadraoDeOportunidadesPagas
    #se opDisfarcadasVis.countSelected > self.plano.quantidadePadraoDeOportunidadesDisfarcadas
    #se é um novo mes, zerar visualizações e serviços solicitados

# @receiver(post_save, sender='auth.User')
# def create_user_cliente(sender, instance, created, **kwargs):
#     if created:
#         Cliente.objects.create(user=instance)
#
# @receiver(post_save, sender='auth.User')
# def save_user_cliente(sender, instance, **kwargs):
#     instance.cliente.save()


@receiver(post_save, sender=Plano)
def update_controle(sender, instance, created, **kwargs):
    controles = ControleDeCliente.objects.filter(plano_id=instance.pk)
    if controles:
        for controle in controles:
            if instance.mesesParaExpirar:
                expiracao = datetime.now() + relativedelta(months=+instance.mesesParaExpirar)
            else:
                expiracao = datetime.now() + relativedelta(days=+instance.diasParaExpirar)
            controle.terminoDeVigenciaDoPlano = expiracao
            controle.plano = instance
            controle.numeroDeVisualizacoesPagas = instance.quantidadePadraoDeOportunidadesPagas
            controle.save()

@receiver(post_save, sender=Cliente)
def create_controle_cliente(sender, instance, created, **kwargs):
    expiracao = None
    if created:
        #enviar email com informações de usuario e senha
        subject, from_email, to = '4Mãos - Bem-vindo! Complete o Seu Cadastro', 'sistema@4maos.com.br', instance.email

        text_content = """

        <html>
      <head>
        <style>
          .body{
            width:50% !important;
          }
          a{
            color: #003366 !important;
            text-decoration: none;
          }
          a:hover{
            text-decoration: underline;
          }
          .lista{
            text-align:right;
            padding: 40px 50px;
          }
          .lista ul{
            list-style: none;
            padding-left: 0;
            float: right;
          }
          .lista ul li{
            float: left;
            color: #fff;
          }
          .lista ul li a{
            text-decoration: none;
            color: #fff !important;
          }
          .lista ul li a:hover{
            text-decoration: underline;
          }
          h2{
            margin: 0 0 17px;
          }

          @media only screen and (max-device-width: 480px), only screen and (max-width: 480px) {
            .body { width:100% !important; }

            .m-shell { width: 100% !important; min-width: 100% !important; }

            .m-center { text-align: center !important; }
            .center { margin: 0 auto !important; }

            .td { width: 100% !important; min-width: 100% !important; }
            .h2 { font-size: 35px !important; line-height: 40px !important; }
            .nav { font-size: 12px !important; line-height: 22px !important; padding: 10px !important; }

            .m-br-15 { height: 15px !important; }
            .p0-15-30 { padding: 0px 15px 30px 15px !important; }
            .p0-20-30 { padding: 0px 20px 30px 20px !important; }
            .p30-0 { padding: 30px 0px !important; }
            .p30-20 { padding: 30px 20px !important; }
            .pb30 { padding-bottom: 30px !important; }
            .p10 { padding: 10px !important; }

            .m-td,
            .m-hide { display: none !important; width: 0 !important; height: 0 !important; font-size: 0 !important; line-height: 0 !important; min-height: 0 !important; }

            .m-block { display: block !important; }

            .fluid-img img { width: 100% !important; max-width: 100% !important; height: auto !important; }

            .column,
            .column-dir,
            .column-top,
            .column-bottom,
            .column-dir-top { float: left !important; width: 100% !important; display: block !important; }

            .content-spacing { width: 15px !important; }
            .lista{
              width: 100% !important;
              text-align: initial !important;
            }
            .lista-dentro{
              float: left !important;
            }
            .lista-dentro ul li{
              margin-right: 20px;
            }
            .lista ul{
            }
            .logo-f{
              display: none !important;
            }
          }
        </style>
      </head>
      <body class='body' style='padding:0 !important; margin:auto !important; display:block !important; background:#f1f1f1; -webkit-text-size-adjust:none;'>


        <table width='100%' border='0' cellspacing='0' cellpadding='0'>
          <tr>
            <td bgcolor='#003366' class='p30-20' style='padding: 40px 50px;'>
              <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                <tr>
                  <th class='column-top' width='120' style='font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; vertical-align:top;'>
                    <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                      <tr>
                        <td class='logo m-center img' style='font-size:0pt; line-height:0pt; text-align:center;'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/logo-4maos-footer.png' width='150' border='0' alt='' /></td>
                      </tr>
                    </table>
                  </th>
                </tr>
              </table>
            </td>
            <td bgcolor='#003366' class='p30-20 lista' style='text-align:right;padding: 40px 50px;'>
              <ul>
                <li><a href='mailto:contato@4maos.com.br'>contato@4maos.com.br</a></li>
              </ul>
            </td>
          </tr>
        </table>


        <table width='100%' border='0' cellspacing='0' cellpadding='0'>
          <tr>
            <td style='padding: 50px;' class='p30-20'>
              <table width='100%' border='0' cellspacing='0' cellpadding='0' style='font-size:14px'>
                <tr>
                  <td class='text' style='padding-bottom: 30px; color:#666666; font-family:'Lato', Arial, sans-serif; font-size:16px; line-height:28px; min-width:auto !important;'>
                    <h2>Olá """+instance.nome+""",</h2>
                    Bem-vindo a plataforma 4 Mãos onde juntos vamos decolar seu escritório contábil!<br/>
                    Para ter acesso a plataforma basta seguir os passos abaixo:<br/><br/>
                    Entre nessa url:<br/>
                    <a href='www.4maos.com.br' target='_blank'>www.4maos.com.br</a><br/>
                    Seu login de acesso é: <strong>"""+instance.usuario.username+"""</strong><br/>
                    Sua senha é: <strong>"""+instance.senhaTemporaria+"""</strong><br/><br/>
                    <b>Se cadastrando gratuitamente veja seus benefícios:</b><br/>
                    Você está atualmente em uma conta gratuita, que lhe permite acessar até 1 oportunidade de negócio em 7 dias úteis gratuitamente, onde vai se conectar ao empreendedor que está buscando um escritório contábil como o seu. Caso queira possuir mais oportunidades e acessar ferramentas de marketing que vão te ajudar a vender mais entre em contato conosco através do e-mail <a href='mailto:contato@4maos.com.br'>contato@4maos.com.br</a><br/><br/>
                    Atenciosamente,<br/>
                    Equipe 4 Mãos
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>


        <table width='100%' border='0' cellspacing='0' cellpadding='0'>
          <tr>
            <td bgcolor='#003366' class='p30-20 logo-f' style='padding: 40px 50px;'>
              <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                <tr>
                  <th class='column-top' width='120' style='font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; vertical-align:top;'>
                    <table width='100%' border='0' cellspacing='0' cellpadding='0'>
                      <tr>
                        <td class='logo m-center img' style='font-size:0pt; line-height:0pt; text-align:center;'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/logo-4maos-footer.png' width='150' border='0' alt='' /></td>
                      </tr>
                    </table>
                  </th>
                </tr>
              </table>
            </td>
            <td bgcolor='#003366' class='p30-20 lista'>
              <div class='lista-dentro'>
                <ul>
                  <li><a href='#'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/fb.png' width='20' height='20'></a></li>
                  <li><a href='#'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/ig.png' width='20' height='20'></a></li>
                  <li><a href='#'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/in.png' width='20' height='20'></a></li>
                  <li><a href='#'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/tt.png' width='20' height='20'></a></li>
                  <li><a href='#'><img src='https://4maos.com.br/wp-content/themes/theme-4maos2/assets/imagens/yt.png' width='20' height='20'></a></li>
                </ul>
              </div>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """ 

        # Olá %s,
        # \nBem-vindo a plataforma 4 Mãos onde juntos vamos decolar seu escritório contábil!
        # \nPara ter acesso a plataforma basta seguir os passos abaixo:
        # \nEntre nessa url: <a href="https://www.4maos.com.br">www.4maos.com.br</a>
        # \nSeu login de acesso é: %s , e sua senha é: %s
        # \nSe cadastrando gratuitamente veja seus benefícios:
        # \n\n\n
        # Você está atualmente em uma conta gratuita, que lhe permite acessar até \n
        # 1 oportunidade de negócio em 7 dias úteis gratuitamente, onde vai se conectar\n
        # ao empreendedor que está buscando um escritório contábil como o seu. \n
        # Caso queira possuir mais oportunidades e acessar ferramentas de marketing \n
        # que vão te ajudar a vender mais entre em contato conosco através do e-mail contato@4maos.com.br
        # \n\n
        # Atenciosamente,
        # \nEquipe 4 Mãos
        # \n<img width="200px" src="https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png">

        instance.usuario.set_password(instance.senhaTemporaria)
        instance.save()

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=("contato@4maos.com.br", "jorge.torrez@4maos.com.br","corina.braga@4maos.com.br","",))  # ghabriel.rodrigues.araujo@gmail
            msg.content_subtype = "html"
            msg.send()

        if instance.plano.mesesParaExpirar:
            expiracao = datetime.now() + relativedelta(months=+instance.plano.mesesParaExpirar)
        else:
            expiracao = datetime.now() + relativedelta(days=+instance.plano.diasParaExpirar)


    else:
        cliente = Cliente.objects.get(usuario__pk=instance.usuario.pk)
        try:
            controle = ControleDeCliente.objects.get(cliente__pk=cliente.pk)
        except:
            pass

        if instance.plano.mesesParaExpirar:
            expiracao = datetime.now() + relativedelta(months=+instance.plano.mesesParaExpirar)
        else:
            if not instance.plano.diasParaExpirar:
                instance.plano.diasParaExpirar=7

            expiracao = datetime.now() + relativedelta(days=+instance.plano.diasParaExpirar)


        #enviar email com informações de usuario e senha
        subject, from_email, to = '4Mãos - Mensagem enviada pelo site', 'sistema@4maos.com.br', instance.email

        text_content = """Olá %s, você alterou seu plano no sistema 4Mãos, seu plano agora é o %s!
        \n\n
        Atenciosamente,
        \nEquipe 4 Mãos
        \n<img width="200px" src='https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png'>
        """ % (instance.nome, instance.plano.nome)

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=("",))  # ghabriel.rodrigues.araujo@gmail
            msg.content_subtype = "html"
            msg.send()

    flag = True

    try:
        contact = ControleDeCliente.objects.get(cliente__pk=cliente.pk)
    except:
        flag = False

    if flag:
        #contact.terminoDeVigenciaDoPlano = expiracao
        #contact.plano = instance.plano
        #if (resetarCredito):
        #  contact.numeroDeVisualizacoesPagas = instance.plano.quantidadePadraoDeOportunidadesPagas
        contact.save()
    else:
        if created:
            ControleDeCliente.objects.create(
                cliente=instance, plano=instance.plano,
                terminoDeVigenciaDoPlano=expiracao,
                numeroDeVisualizacoesPagas=instance.plano.quantidadePadraoDeOportunidadesPagas)
