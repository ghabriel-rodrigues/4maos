from django import forms
from django.conf import settings

from django.core.mail import EmailMultiAlternatives, send_mail
from .models import Oportunidade, Plano, ConteudoEducativo, DuvidasSobreOportunidades, DuvidasFrequentes, Necessidades, TratativasDeOportunidades
from cliente.models import ControleDeCliente, NegociacoesDeOportunidades, Cliente


class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        exclude = ('autor','dataDeCadastro',)
        widgets = {'dataDeSolicitacao': forms.SelectDateWidget(),
        'dataDeFinalizacao': forms.SelectDateWidget(),'dataDePublicacao': forms.SelectDateWidget(),}
        # fields = ('tipoDeOportunidade', 'status', 'autor', 'nome', 'empresa',
        #   'cnpj', 'telefone', 'email', 'bairro', 'cidade', 'preferencia', 'grauDeUrgencia',
        #   'numeroDeParticipantes', 'servicoSolicitado', 'tipoDeCliente', 'observacoes',
        #   'dataDeSolicitacao', 'dataDeFinalizacao', 'dataDePublicacao',)

    # def save(self, commit=True):
    #     lead = super(OportunidadeForm, self).save(commit=False)
    #     if lead.tipoDeOportunidade == "disfarcada":
    #         subject, from_email, to = '4Mãos - Mensagem enviada pelo site', 'sistema@4maos.com.br', 'leandrohilariovenancio@gmail.com' # ghabriel.rodrigues.araujo@gmail
    #
    #         text_content = """Olá, você recebeu uma resposta sobre a oportunidade disfarçada, que segue abaixo: \n \n %s , e sua senha é: %s""" % (instance.nome, instance.usuario.username, instance.usuario.password)
    #
    #         if settings.ONLINE
    #             msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #             msg.send()
    #
    #     if commit:
    #         lead.save()
    #
    #     return lead

class DuvidaForm(forms.ModelForm):
    class Meta:
        model = DuvidasSobreOportunidades
        exclude = ('autor','dataDeCadastro',)

class DuvidaFrequenteForm(forms.ModelForm):
    class Meta:
        model = DuvidasFrequentes
        exclude = ('autor','dataDeCadastro',)

class NecessidadeForm(forms.ModelForm):
    class Meta:
        model = Necessidades
        exclude = ('autor','dataDeCadastro',)

    def enviar(self, need):
        subject, from_email, to = '4Mãos - Dúvida enviada pelo site!', 'sistema@4maos.com.br', 'contato@4maos.com.br'

        text_content = """Olá Administrador 4Mãos, o cliente %s enviou a seguinte dúvida: \nNome:%s \nEmail:%s \nAssunto:%s \nTelefone:%s \nMensagem:\n%s""" % (need.autor.email, need.nome, need.email, need.assunto, need.telefone, need.mensagem)

        if settings.ONLINE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc=('',))  # ghabriel.rodrigues.araujo@gmail
            msg.send()

class TratativaForm(forms.ModelForm):
    class Meta:
        model = TratativasDeOportunidades
        exclude = ('autor','dataDeCadastro','oportunidadeRelacionada')
        widgets = {'dataDoProximoContato': forms.SelectDateWidget()}

class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        exclude = ('autor','dataDeCadastro',)

class ConteudoEducativoForm(forms.ModelForm):
    class Meta:
        model = ConteudoEducativo
        exclude = ('autor','dataDeCadastro',)

class UploadConteudoForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
