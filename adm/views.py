from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ConteudoEducativo, Oportunidade, Plano
from .forms import OportunidadeForm, NecessidadeForm, PlanoForm
from cliente.models import Cliente
from cliente.forms import ProfileForm, UserForm
import csv
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

def exportar_clientes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)

    writer.writerow(['ID','STATUS', 'EMAIL', 'CPF', 'NOME', 'SOBRENOME', 'CARGO', 'DEPARTAMENTO',
        'RG', 'CNPJ', 'RAZAO SOCIAL', 'NOME DO RESPONSAVEL', 'CRC DO RESPONSAVEL', 'CPF DO RESPONSAVEL',
        'TIPO DE ESCRITORIO','AREA DE ATUACAO','CEP','RUA','NUMERO','BAIRRO','CIDADE','TELEFONE','CARTAO CREDITO',
        'NOME TITULAR','DATA VALIDADE','CVV','PLANO','DATA DE CADASTRO',])

    clientes = Cliente.objects.all().values_list('id','status', 'email', 'cpf', 'nome', 'sobrenome', 'cargo', 'departamento',
    'rg', 'cnpj', 'razaoSocial', 'nomeDoResponsavel', 'crcDoResponsavel', 'cpfDoResponsavel',
    'tipoDeEscritorio','areaDeAtuacao','cep','rua','numero','bairro','cidade','telefone','cartaoCredito',
    'nomeTitular','dataValidade','cvv','plano','dataDeCadastro')

    for cliente in clientes:
        writer.writerow(cliente)

    return response

def test():
    clientes = Cliente.objects.exclude(status='Inativo').exclude(status='Inativo - Cancelado')
    list1 = []
    oportunidadesPagas = Oportunidade.objects.filter(tipoDeOportunidade='paga').filter(dataDePublicacao__lte=timezone.now()).exclude(status="Aguardando publicação").exclude(status="Finalizado").order_by('-dataDeCadastro')
    listaDeOportunidades = ""
    i = 0

    for oportunidade in oportunidadesPagas:
        if i <= 3:
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

    for clienteNewsletter in clientes:
        subject, from_email, to = '4Mãos - Mensagem enviada pelo site', 'sistema@4maos.com.br', clienteNewsletter.email
        list1 = [to]

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=list1, bcc=("",))  # ghabriel.rodrigues.araujo@gmail
            msg.content_subtype = "html"
            msg.send()

    return locals()

def admin_cadastro_clientes(request):
    variaveis = test()
    if request.method == "POST":
        clienteForm = ProfileForm(request.POST)
        if clienteForm.is_valid():
            cliente = clienteForm.save(commit=False)
            cliente.autor = request.user
            cliente.dataDeCadastro = timezone.now()
            cliente.save()
            enviado = True
    else:
        clienteForm = ProfileForm()



    return render(request, 'adm/admin-cadastro-clientes.html', variaveis)

def admin_cliente_edit(request, pk):
     cliente = get_object_or_404(Cliente, pk=pk)

     if request.method == 'POST':
         user_form = UserForm(request.POST, instance=request.user)
         profile_form = ProfileForm(request.POST, instance=request.user.cliente)
         if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
             # messages.success(request, _('Your profile was successfully updated!'))
             # return redirect('settings:profile')
         else:
             pass
             # messages.error(request, _('Please correct the error below.'))
     else:
         user_form = UserForm(instance=request.user)
         profile_form = ProfileForm(instance=request.user.cliente)

     return render(request, 'adm/admin-cliente-edit.html', locals())

def admin_controle_acesso(request):
    planos = Plano.objects.all()
    planoForm = PlanoForm()
    if request.method == "POST":
        planoForm = PlanoForm(request.POST)
        if planoForm.is_valid():
            plano = planoForm.save(commit=False)
            plano.autor = request.user
            plano.dataDeCadastro = timezone.now()
            plano.save()
            enviado = True
    else:
        planoForm = PlanoForm()
    return render(request, 'adm/admin-controle-acesso.html', locals())

def admin_gestao_oportunidades(request):
    oportunidades = Oportunidade.objects.all()
    return render(request, 'adm/admin-gestao-oportunidades.html', locals())

def admin_upload_oportunidades(request):
    if request.method == "POST":
        oportunidadeForm = OportunidadeForm(request.POST)
        if oportunidadeForm.is_valid():
            oportunidade = oportunidadeForm.save(commit=False)
            oportunidade.autor = request.user
            oportunidade.dataDeCadastro = timezone.now()
            oportunidade.save()
            enviado = True
    else:
        oportunidadeForm = OportunidadeForm()
    return render(request, 'adm/admin-upload-oportunidades.html', locals())

def admin_upload_oportunidades_disfarcadas(request):
    return render(request, 'adm/admin-upload-oportunidades-disfarcadas.html', {})

def admin_conteudo_educativo(request):
    return render(request, 'adm/admin-upload-conteudo-educativo.html', locals())

def admin_upload_marketing_apoio(request):
    return render(request, 'adm/admin-upload-marketing-apoio.html', {})

def admin_upload_marketing_avancado(request):
    multipleFileForm = UploadConteudoForm()
    uploads = UploadConteudo.objects.all().filter(status='ativo').filter(tipoDeUpload__titulo="Material de Marketing Avançado")
    return render(request, 'adm/admin-upload-marketing-avancado.html', locals())


#     from django.views.generic.edit import FormView
# from .forms import FileFieldForm
#
# class FileFieldView(FormView):
#     form_class = FileFieldForm
#     template_name = 'upload.html'  # Replace with your template.
#     success_url = '...'  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 ...  # Do something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
