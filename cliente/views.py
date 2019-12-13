from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Cliente, Plano, ControleDeCliente, NegociacoesDeOportunidades
from .forms import ProfileForm, UserForm, FirstProfileForm
from .filters import OportunidadeFilter
from adm.models import (DuvidasFrequentes, DuvidasSobreOportunidades, Servico, MaterialDeApoioBasico,
                        Oportunidade, TratativasDeOportunidades, ConteudoEducativo,
                        MaterialDeMarketingAvancado, Arquivo)
from adm.forms import NecessidadeForm, TratativaForm, DuvidaForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
import base64
from django.core.files.base import ContentFile

from PIL import Image

@login_required
def material_marketing_apoio(request):
    materialApoio = get_object_or_404(MaterialDeApoioBasico)
    return render(request, 'cliente/cliente-material-marketing-apoio.html', locals()) #'oportunidades': oportunidades

@login_required
def material_marketing_avancado(request):
    materialAvancado = get_object_or_404(MaterialDeMarketingAvancado)
    return render(request, 'cliente/cliente-material-marketing-avancado.html', locals()) #'oportunidades': oportunidades

@login_required
def conteudo_educativo(request):
    conteudoEducativo = get_object_or_404(ConteudoEducativo)
    necessidadeForm = NecessidadeForm()
    if request.method == "POST":
        necessidadeForm = NecessidadeForm(request.POST)
        if necessidadeForm.is_valid():
            need = necessidadeForm.save(commit=False)
            need.autor = request.user
            need.dataDeCadastro = timezone.now()
            need.save()
            necessidadeForm.enviar(need)
        else:
            necessidadeForm = NecessidadeForm()
    return render(request, 'cliente/cliente-conteudo-educativo.html', locals())

@login_required
def perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.cliente)
        if user_form.is_valid() and profile_form.is_valid():
            senha = request.POST.get('senhaTemporaria')
            user = user_form.save()
            profile = profile_form.save()
            logo = request.POST.get('logo')

            if logo:
              formatting = logo.split(';base64,')[0] 
              imgstr = logo.split(';base64,')[1] 
              ext = formatting.split('/')[-1] 
              filename = request.POST.get('logo_name')
              logo = ContentFile(base64.b64decode(imgstr), name= filename+'.' + ext)

              cliente = Cliente.objects.get(usuario=request.user)
              cliente.logo.save(filename,logo)
              cliente.save()

            user.set_password(profile.senhaTemporaria)
            user.save()

            update_session_auth_hash(request, user)
        
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.cliente)

    return render(request, 'cliente/cliente-perfil.html', locals())

@login_required
@csrf_exempt
def crop_logo(request):
    return render(request, 'cliente/crop_logo.html', locals())

@login_required
@csrf_exempt
def salvar_logo(request):
  if request.method == 'POST':
    cliente = Cliente.objects.get(usuario=request.user)
    logo = request.POST.get('url')+"="
    filename = request.POST.get('filename')
    url_decoded = base64.b64decode(logo)        
    content = ContentFile(url_decoded) 
    cliente.logo.save(filename,content)
    cliente.save()
    

  return render(request, 'cliente/salvar-logo.html', locals())

    

@login_required
def duvidas_frequentes(request):
    duvidas = DuvidasFrequentes.objects.all()
    necessidadeForm = NecessidadeForm()
    if request.method == "POST":
        necessidadeForm = NecessidadeForm(request.POST)
        if necessidadeForm.is_valid():
            need = necessidadeForm.save(commit=False)
            need.autor = request.user
            need.dataDeCadastro = timezone.now()
            need.save()
            necessidadeForm.enviar(need)
        else:
            necessidadeForm = NecessidadeForm()
    return render(request, 'cliente/cliente-duvidas-frequentes.html', locals()) 

@login_required
def logout(request):
    return render(request, 'cliente/cliente-logout.html', {}) 

@login_required
@csrf_exempt
def oportunidades(request):
    cliente = False
    try:
      cliente = Cliente.objects.get(usuario=request.user)
    except:
      clienteErro = True

    oportunidades = OportunidadeFilter(request.GET, queryset=Oportunidade.objects.exclude(status="Aguardando publicação").exclude(status="Finalizado").exclude(dataDeFinalizacao__lte=timezone.now()).filter(dataDePublicacao__lte=timezone.now()).filter(tipoDeOportunidade='paga').order_by('dataDeCadastro'))
    leadsComNegociacoes = []
    leadsSemNegociacoes = []
    for oportunidade in oportunidades.qs:
        negociacoes = NegociacoesDeOportunidades.objects.filter(cliente=cliente).filter(oportunidade=oportunidade)
        numeroDeNegociacoes = negociacoes.count()
        if numeroDeNegociacoes >= 1:
            leadsComNegociacoes.append(oportunidade.id)
        else:
            leadsSemNegociacoes.append(oportunidade.id)


    necessidadeForm = NecessidadeForm()
    if request.method == "POST":
        necessidadeForm = NecessidadeForm(request.POST)
        if necessidadeForm.is_valid():
            need = necessidadeForm.save(commit=False)
            need.autor = request.user
            need.dataDeCadastro = timezone.now()
            need.save()
            necessidadeForm.enviar(need)
        else:
            necessidadeForm = NecessidadeForm()   
    return render(request, 'cliente/cliente-oportunidades.html', locals())



# @csrf_protect
@login_required
@csrf_exempt
def oportunidade_falar(request, pk):
    cliente = Cliente.objects.get(usuario=request.user)
    controle = ControleDeCliente.objects.get(cliente__pk=cliente.pk)
    totalParticipantes = NegociacoesDeOportunidades.objects.filter(oportunidade__pk=pk).count()
    oportunidade = get_object_or_404(Oportunidade, pk=pk)
    erro = ""
    temNegociacao = False
    negociacoes = NegociacoesDeOportunidades.objects.filter(cliente=cliente).filter(oportunidade=oportunidade)

    if controle.autorizaComunicacaoPagas() == 1:
        if totalParticipantes < oportunidade.numeroDeParticipantes:

            if negociacoes.count() > 0:
                temNegociacao = True
            else:
                negociacao = NegociacoesDeOportunidades()
                negociacao.cliente = cliente
                negociacao.oportunidade = oportunidade
                negociacao.status =  'Aguardando posicionamento'
                negociacao.controleDeCliente = controle
                negociacao.save()
                controle.decrementarNumeroDeVisualizacoesPagas()
                controle.save()

                subject, from_email, to = 'Plataforma 4 Mãos - Sua oportunidade foi visualizada', 'empreendedores@4maos.com.br', [oportunidade.email]

                text_content = """Olá %s, Obrigado por utilizar a plataforma 4 Mãos, informamos que um contador acabou de visualizar sua solicitação de orçamento em breve ele entrará em contato.</br></br>
                </br></br></br>Pedimos apenas a gentileza de prestar o feedback para cada contador, porque eles pagam para te atender, então pedimos somente essa gentileza.
                </br></br></br>Atenciosamente,
                </br>Atendimento empreendedores@4maos.com.br
                </br>
                """ % (controle.cliente.nome)

                if settings.ONLINE:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                    msg.content_subtype = "html"
                    msg.send()
        else:
            if negociacoes.count() > 0:
                temNegociacao = True
            else:
                erro="Você não foi autorizado a se comunicar com a oportunidade pois o número total de participantes já foi atingido."
                oportunidade = False
    elif controle.autorizaComunicacaoPagas() == 2:
        # as visualizações do cliente não podem ser maiores que as default do seu proprio plano
        erro="Você não foi autorizado a se comunicar com a oportunidade por uma incoerência de dados entre sua conta e seu plano. Entre em contato com a administração."
        oportunidade = False
    elif controle.autorizaComunicacaoPagas() == 3:
        if not negociacoes:
            oportunidade = False
            erro="Você não foi autorizado a se comunicar com a oportunidade pois suas visualizações das oportunidades pagas acabaram."

    elif controle.autorizaComunicacaoPagas() == 4:
        erro="Você não foi autorizado a se comunicar com a oportunidade pois o tempo de seu plano expirou."
        oportunidade = False
    else:
        # as visualizações do cliente não podem ser maiores que as default do seu proprio plano
        erro="Você não foi autorizado a se comunicar com a oportunidade por uma incoerência de dados entre sua conta e seu plano. Entre em contato com a administração."
        oportunidade = False

    return render(request, 'cliente/cliente-oportunidades-falar.html', locals()) #'oportunidade': oportunidade


@login_required
def oportunidades_disfarcadas(request):
    oportunidadesDisf = Oportunidade.objects.filter(dataDePublicacao__lte=timezone.now()).filter(tipoDeOportunidade='disfarcada').order_by('dataDeCadastro').exclude(status="Aguardando publicação").exclude(status="Finalizado")
    duvidaForm = DuvidaForm()
    opDisfExcluir = []
    duvidas = DuvidasSobreOportunidades.objects.all()

    if request.method == "POST":
        cliente = Cliente.objects.get(usuario=request.user)
        controle = ControleDeCliente.objects.get(cliente__pk=cliente.pk)
        totalParticipantes = NegociacoesDeOportunidades.objects.filter(oportunidade__pk=request.POST.get('oportunidadeRelacionada')).count()
        oportunidade = Oportunidade.objects.get(pk=request.POST.get('oportunidadeRelacionada'))
        duvidaForm = DuvidaForm(request.POST)
        if duvidaForm.is_valid():
            need = duvidaForm.save(commit=False)
            need.autor = request.user
            need.oportunidadeRelacionada = Oportunidade.objects.get(pk=request.POST.get('oportunidadeRelacionada'))
            need.dataDeCadastro = timezone.now()
            need.save()

            subject, from_email, to = '4Mãos - Resposta de um contador', 'sistema@4maos.com.br', oportunidade.email

            text_content = """
            </br>Olá Empreendedor,</br>
            </br>
            </br>Segue abaixo a resposta de um dos contadores cadastradores na plataforma 4 Mãos,
            </br>veja que possui o contato do mesmo e você pode aprofundar sua dúvida respondendo o mesmo diretamente.
            </br>Nome: %s </br>Telefone: %s </br>Email: %s </br>Resposta: %s</br>
            </br>
            </br>
            </br>Esperamos que a resposta tenha esclarecido sua dúvida,
            </br>caso contrário ratificamos para falar diretamente com o mesmo
            </br>ou deixar nova pergunta através do site <a href="www.4maos.com.br/empreendor">www.4maos.com.br/empreendor</a>
            </br></br>
            Atenciosamente,
            </br>Equipe 4 Mãos
            </br><img width="200px" src='https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png'>
            """ % (cliente.nome, cliente.telefone, cliente.email, need.descricao)

            if settings.ONLINE:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to,], bcc=('',))  # ghabriel.rodrigues.araujo@gmail
                msg.content_subtype = "html"
                msg.send()

            msg = "Envio feito com sucesso!"

    return render(request, 'cliente/cliente-oportunidades-disfarcadas.html', locals())


@login_required
def oportunidade_detail(request, pk):
    return render(request, 'cliente/oportunidade_detail.html', {}) #'oportunidade': oportunidade

@login_required
def oportunidade_new(request):
     return render(request, 'cliente/oportunidade_edit.html', {}) #'form': form

@login_required
def oportunidade_edit(request, pk):
     return render(request, 'cliente/oportunidade_edit.html', {}) #'form': form

@login_required
def servico_detail(request, link):
    cliente = Cliente.objects.get(usuario=request.user)
    servicoPage = get_object_or_404(Servico, link=link)
    servicosGaleria = Servico.objects.filter(categoria__pk=servicoPage.categoria.pk)
    servicosPorCategoria = Servico.objects.filter(categoria__pk=servicoPage.categoria.pk).order_by('-dataDeCadastro')

    necessidadeForm = NecessidadeForm()
    if request.method == "POST":
        necessidadeForm = NecessidadeForm(request.POST)
        if necessidadeForm.is_valid():
            need = necessidadeForm.save(commit=False)
            need.autor = request.user
            need.dataDeCadastro = timezone.now()
            need.save()
            necessidadeForm.enviar(need)
        else:
            necessidadeForm = NecessidadeForm()
    return render(request, 'cliente/servico-detail.html', locals())

@login_required
def planos(request):
    return render(request, 'cliente/cliente-planos.html', locals())

def firstprofile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)        
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'cliente/cliente-firstprofile.html', locals())


def checarControle(controle):
    if controle.checarSeAcabouPlano():
        controle.cliente.status = 'Inativo'
        controle.cliente.save()
        subject, from_email, to = '4Mãos - Seu usuário se tornou inativo', 'sistema@4maos.com.br', [controle.cliente.email]

        text_content = """Olá %s, seu usuário se tornou inativo pois a data limite de seu plano acabou, renove para continuar tendo acesso ao sistema!</br></br>
        </br></br></br>Atenciosamente,
        </br>Equipe 4 Mãos
        </br>
        """ % (controle.cliente.nome)

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.content_subtype = "html"
            msg.send()

    if controle.diasParaPlanoExpirar() <=5:
        dias = controle.diasParaPlanoExpirar
        subject, from_email, to = '4Mãos - Faltam %s dias para seu plano expirar'%(dias), 'sistema@4maos.com.br', [controle.cliente.email]

        if controle.plano.diasParaExpirar == 7:
            text_content ="""
            </br>Olá Contador(a),
            </br>Viemos gentilmente informar que seu plano gratuito está acabando.
            </br>Não deixei de contatar outros empreendedores que estão buscando os seus serviços,
            </br>para isso é necessário contratar um dos nossos planos entrando em contato através do e-mail:
            </br>contato@4maos.com.br
            </br>Veja as vantagens de contratar a plataforma:
            </br>- Encontre empreendedores no momento exato que ele está buscando contadores.
            </br>- Escolha a oportunidade que realmente te interessa.
            </br>- Pare de pagar por ações de marketing que não dão retorno de vendas.
            </br>- Pare de perder tempo buscando aprender marketing. Deixe que trazemos as oportunidades pra você.
            </br>- Tenha toda solução de marketing para seu escritório em um único lugar com investimentos acessíveis.
            </br>- Encontre oportunidades de vender no meio de dúvidas de empreendedores gratuitamente.
            </br>- Tenha acesso as principais notícias de transformação digital para contadores.
            </br>- Não perca mais tempo fale conosco agora mesmo através do e-mail: contato@4maos.com.br que um consultor entrará em contato para esclarecimentos.
            </br></br>
            Atenciosamente,
            </br>Equipe 4 Mãos
            """

            text_content = returnEmailTemplate(text_content)
        else:
            text_content = """
            </br>Olá contador (a), seu usuário se tornará inativo pois a data limite de seu plano está chegando ao fim, renove para continuar tendo acesso ao sistema!
            </br></br>
            Atenciosamente,
            </br>Equipe 4 Mãos
            """
            text_content = returnEmailTemplate(text_content)

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=[to])
            msg.content_subtype = "html"
            msg.send()

    if controle.checarSeAcabouVigenciaMensal():
        #controle.numeroDeVisualizacoesPagas = controle.plano.quantidadePadraoDeOportunidadesPagas
        #controle.numeroDeVisualizacoesDisfarcadas = controle.plano.quantidadePadraoDeOportunidadesDisfarcadas

        controle.save()

def returnEmailTemplate(content):
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
                """+content+"""
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
</html>"""
    return text_content

def cronjob(request):
    request.META['HTTP_X_CRON_AUTH'] = 'c68c2eb130be4d45522e2e7bcb2fed32'
    # text_content = enviarLeads()

    clientes = Cliente.objects.exclude(status='Inativo').exclude(status='Inativo - Cancelado')
    list1 = []

    oportunidadesPagas = Oportunidade.objects.filter(tipoDeOportunidade='paga').filter(dataDePublicacao__lte=timezone.now()).exclude(dataDeFinalizacao__lte=timezone.now()).exclude(status="Aguardando publicação").exclude(status="Finalizado").order_by('-dataDeCadastro')
    listaDeOportunidades = ""
    i = 0

    for oportunidade in oportunidadesPagas:

        oportunidadeSTRING = """</br></br>
        <h2>%s</h2></br>
        <b>Nome: </b>%s</br>
        <b>Finaliza em: </b>%s</br>
        <b>Tipo de empresa: </b>%s</br>
        <b>Cidade: </b>%s</br>
        <b>Bairro: </b>%s</br>
        <b>Grau de Urgência: </b>%s</br>
        <b>Preferência: </b>%s</br>
        <b>Data da solicitação: </b>%s</br>
        <b>Número de participantes dessa oportunidade: </b>%s/%s</br>
        </br></br>
        """ %(oportunidade.nome, oportunidade.primeiroNome, oportunidade.dataDeFinalizacao,
         oportunidade.tipoDeEmpresa, oportunidade.cidade, oportunidade.bairro, oportunidade.grauDeUrgencia,
          oportunidade.preferencia, oportunidade.dataDeSolicitacao, oportunidade.numeroDeParticipantes,
           oportunidade.getTotalParticipantes,)
        listaDeOportunidades = listaDeOportunidades + oportunidadeSTRING +"</br>"
        i=i+1

    clientes = Cliente.objects.exclude(status='Inativo').exclude(status='Inativo - Cancelado')

    to = []

    for clienteNewsletter in clientes:
        #avisar usuarios sobre oportunidades
        subject = '4Mãos - Oportunidades exclusivas!'
        from_email = 'sistema@4maos.com.br'
        to = [clienteNewsletter.email]

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
                    <h2>Olá, tudo bem?</h2>
                    </br>Como sabem somos uma plataforma de conexão entre contadores e empreendedores,
                    </br>veja abaixo algumas das oportunidades que estão disponíveis nesse exato momento
                    </br>para crescer sua carteira de clientes. Caso queira atender essas oportunidades
                    </br>faça o login em nosso portal através desse link: <a href="https://www.4maos.com.br">www.4maos.com.br</a>

                    """+listaDeOportunidades+"""
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
    </html>"""

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.content_subtype = "html"
            msg.send()

        controle = ControleDeCliente.objects.get(cliente__pk=clienteNewsletter.pk)

        if controle.checarSeAcabouPlano():
            # enviar email
            controle.cliente.status = 'Inativo'
            controle.cliente.save()
            subject, from_email, to = '4Mãos - Seu usuário se tornou inativo', 'sistema@4maos.com.br', controle.cliente.email

            text_content = """Olá %s, seu usuário se tornou inativo pois a data limite de seu plano acabou, renove para continuar tendo acesso ao sistema!</br></br>
            </br></br></br>Atenciosamente,
            </br>Equipe 4 Mãos
            </br><img width="200px" src='https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png'>
            """ % (controle.cliente.nome)

            if settings.ONLINE:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.content_subtype = "html"
                msg.send()

        if controle.diasParaPlanoExpirar() <=5:
            subject, from_email, to = '4Mãos - Faltam '+controle.diasParaPlanoExpirar+' dias para seu plano expirar', 'sistema@4maos.com.br', controle.cliente.email

            if controle.plano.diasParaExpirar() == 7:
                text_content ="""
                </br>Olá Contador(a),
                </br>Viemos gentilmente informar que seu plano gratuito está acabando.
                </br>Não deixei de contatar outros empreendedores que estão buscando os seus serviços,
                </br>para isso é necessário contratar um dos nossos planos entrando em contato através do e-mail:
                </br>contato@4maos.com.br
                </br>Veja as vantagens de contratar a plataforma:
                </br>- Encontre empreendedores no momento exato que ele está buscando contadores.
                </br>- Escolha a oportunidade que realmente te interessa.
                </br>- Pare de pagar por ações de marketing que não dão retorno de vendas.
                </br>- Pare de perder tempo buscando aprender marketing. Deixe que trazemos as oportunidades pra você.
                </br>- Tenha toda solução de marketing para seu escritório em um único lugar com investimentos acessíveis.
                </br>- Encontre oportunidades de vender no meio de dúvidas de empreendedores gratuitamente.
                </br>- Tenha acesso as principais notícias de transformação digital para contadores.
                </br>- Não perca mais tempo fale conosco agora mesmo através do e-mail: contato@4maos.com.br que um consultor entrará em contato para esclarecimentos.
                </br></br>
                Atenciosamente,
                </br>Equipe 4 Mãos
                </br><img width="200px" src='https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png'>
                """
            else:
                text_content = """
                </br>Olá contador (a), seu usuário se tornará inativo pois a data limite de seu plano está chegando ao fim, renove para continuar tendo acesso ao sistema!
                </br></br>
                Atenciosamente,
                </br>Equipe 4 Mãos
                </br><img width="200px" src='https://4maos.com.br/quatromaos/static/assets/img/logo-4maos-azul.png'>
                """

            if settings.ONLINE:
                msg = EmailMultiAlternatives(subject, text_content, from_email, to=list1)
                msg.content_subtype = "html"
                msg.send()

        #if controle.checarSeAcabouVigenciaMensal():
        #    controle.numeroDeVisualizacoesPagas = controle.plano.quantidadePadraoDeOportunidadesPagas

    text_content = returnEmailTemplate(listaDeOportunidades)

    for clienteNewsletter in clientes:
        subject, from_email, to = '4Mãos - Mensagem enviada pelo site', 'sistema@4maos.com.br', clienteNewsletter.email
        list1 = [to]

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=list1, bcc=("",)) # ghabriel.rodrigues.araujo@gmail
            msg.content_subtype = "html"
            msg.send()

        controle = ControleDeCliente.objects.get(cliente__pk=clienteNewsletter.pk)
        checarControle(controle)

    return render(request, 'cliente/cliente-cronjob.html', locals())
