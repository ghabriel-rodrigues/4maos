from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from .models import Cliente, ControleDeCliente
from django.utils import timezone
import base64
import re
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    #    widgets = {'password': forms.PasswordInput()}

class FirstProfileForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length = 255,required=True)
    sobrenome = forms.CharField(label="Sobrenome", max_length = 255,required=True)
    cpf = forms.CharField(label="CPF", max_length = 255,required=True)
    razaoSocial = forms.CharField(label="Razão Social / Nome da empresa", max_length = 255,required=True)
    email = forms.CharField(label="Usuário (email)", max_length = 255,required=True)
    senhaTemporaria = forms.Field(widget=forms.PasswordInput(), label="Senha", required=True)

    assunto = forms.CharField(label="Assunto", max_length = 255,required=True)
    impede = forms.Field(widget=forms.Textarea,label="O que te impede de crescer?",required=True)
    #aceita = forms.BooleanField(label="Concordo com os termos de uso",required=True)



    # def save(self, commit=True):
    #     usuario = super(FirstProfileForm, self).save(commit=False)
    #     usuario.set_password(self.cleaned_data['password'])
    #     usuario.username = self.cleaned_data['email']
    #
    #     if commit:
    #         usuario.save()
    #
    #     return usuario



class ProfileForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ('username','usuario','dataDeCadastro', 'plano')
        widgets = {'dataValidade': forms.SelectDateWidget()}

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'],).count():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este LOGIN')
        return self.cleaned_data['username']

    # def clean_telefone(self):
    #     num = self.cleaned_data['telefone'][5:6]
    #     if num != "6" and num != "7" and num != "8" and num != "9":
    #         raise forms.ValidationError('Por favor insira um numero de celular valido')
    #         #raise forms.ValidationError(self.cleaned_data['telefone'][5:6])
    #     return self.cleaned_data['telefone']

    # def clean_email(self):
    #
    #     if User.objects.filter(email=self.cleaned_data['email'],).count():
    #         raise forms.ValidationError('Ja existe um usuario cadastrado com este EMAIL')
    #     return self.cleaned_data['email']

    # def clean_rg(self):
    #    if Cliente.objects.filter(rg=self.cleaned_data['rg'],).count():
    #        raise forms.ValidationError('Ja existe um usuario cadastrado com este RG')
    #    return self.cleaned_data['rg']

    # def clean_cpf(self):
    #     if Cliente.objects.filter(cpf=self.cleaned_data['cpf'],).count():
    #         raise forms.ValidationError('Ja existe um usuario cadastrado com este CPF')
    #     else:
    #         try:
    #             cpf = CPF(self.cleaned_data['cpf'])
    #             if cpf.valido():
    #                 return self.cleaned_data['cpf']
    #             else:
    #                 raise forms.ValidationError('Por favor informe um CPF valido')
    #         except:
    #             raise forms.ValidationError('Por favor informe um CPF valido')
    #     return self.cleaned_data['cpf']

    def clean_confirme(self):
        if self.cleaned_data['confirme'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere, por favor verifique se a senha e o confirme estao iguais')
        return self.cleaned_data['confirme']
