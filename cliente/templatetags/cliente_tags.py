from django import template

from adm.models import Arquivo
from cliente.models import get_logo_path
from os import path

from django.utils import safestring
from django.conf import settings


register = template.Library()


@register.simple_tag()
def get_arquivo(servico, cliente):
    arquivo = Arquivo.objects.filter(galeria_arquivos__servico_galeria=servico.pk)
    
    botao = '<a class="file-download" href="%s" download="%s">Download</a>'
    choices_coordenadas = ''
   
    if arquivo.exists():
        arquivo = arquivo.last()
        name = path.basename(arquivo.arquivo.name)
        retorno = botao % (arquivo.arquivo.url, name)
        url = ''

        if settings.ONLINE:
            if cliente.logo:
                url = cliente.logo.url
            else:
                url = '#undefined'
        else:
            if cliente.logo:
                url = get_logo_path(cliente.logo,cliente.logo.url)
            else:
                url = '#undefined'

        if arquivo.choices_coordenadas == 'Canto superior direito':
            choices_coordenadas = 'Canto superior direito'
        if arquivo.choices_coordenadas == 'Canto superior esquerdo':
            choices_coordenadas = 'Canto superior esquerdo'
        if arquivo.choices_coordenadas == 'Canto inferior direito':
            choices_coordenadas = 'Canto inferior direito'
        if arquivo.choices_coordenadas == 'Canto inferior esquerdo':
            choices_coordenadas = 'Canto inferior esquerdo'
        if arquivo.choices_coordenadas == 'Centro':
            choices_coordenadas = 'Centro'

        

        if choices_coordenadas != '':
            botao = '<a  class="file-download" data-href="%s" data-url-logo="%s" download="%s" data-coordenadas="%s" id=file%s>Download</a>'#href="%s"
        
            retorno = botao % (arquivo.arquivo.url, url, name, choices_coordenadas, arquivo.id)
    else:
        if choices_coordenadas != '':
            retorno = botao % ('#', '', '', '', '')
        else:
            retorno = botao % ('#', '')

    return safestring.mark_safe(retorno)


register.filter()