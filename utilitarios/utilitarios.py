#-*- coding: utf-8 -*-
import os
from django.conf import settings

from cliente.models import Cliente, ControleDeCliente
from adm.forms import NecessidadeForm
from adm.models import Oportunidade
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives, send_mail

def utilitarios(request):
    site = None
    cliente = None
    online = True
    usuario = None
    controle = None
    necessidadeForm = NecessidadeForm()

    # oportunidades = OportunidadeFilter(request.GET, queryset=Oportunidade.objects.exclude(status="Aguardando publicação").exclude(status="Finalizado").exclude(dataDeFinalizacao__lte=timezone.now()).filter(dataDePublicacao__lte=timezone.now()).filter(tipoDeOportunidade='paga').order_by('dataDeCadastro'))
    # leadsComNegociacoes = []
    # leadsSemNegociacoes = []
    # for oportunidade in oportunidades.qs:
    #     negociacoes = NegociacoesDeOportunidades.objects.filter(cliente=cliente).filter(oportunidade=oportunidade)
    #     numeroDeNegociacoes = negociacoes.count()
    #     if numeroDeNegociacoes >= 1:
    #         leadsComNegociacoes.append(oportunidade.id)
    #     else:
    #         leadsSemNegociacoes.append(oportunidade.id)
    
    # oportunidadesPagas = Oportunidade.objects.filter(tipoDeOportunidade='paga').filter(dataDePublicacao__lte=timezone.now()).exclude(status="Aguardando publicação").exclude(dataDeFinalizacao__lte=timezone.now()).exclude(status="Finalizado").order_by('-dataDeCadastro')

    totalOportunidadesPagas2 = Oportunidade.objects.filter(tipoDeOportunidade='paga').exclude(dataDeFinalizacao__lte=timezone.now()).filter(dataDePublicacao__lte=timezone.now()).exclude(status="Aguardando publicação").exclude(status="Finalizado")

    totalOportunidadesDisfarcadas2 = Oportunidade.objects.filter(tipoDeOportunidade='disfarcada').filter(dataDePublicacao__lte=timezone.now()).exclude(status="Aguardando publicação").exclude(status="Finalizado")

    totalOportunidadesPagas = 0
    totalOportunidadesAtivas = 0
    totalOportunidadesDisfarcadas = 0

    for lead in totalOportunidadesPagas2:
        if lead.isTotalMenorQueNumeroView():
            totalOportunidadesPagas +=1

    for lead in totalOportunidadesDisfarcadas2:
        if lead.isTotalMenorQueNumeroView() and not lead.temDuvidas():
            totalOportunidadesDisfarcadas +=1

    totalOportunidadesAtivas = totalOportunidadesPagas + totalOportunidadesDisfarcadas

    try:
        usuario = request.user
        cliente = Cliente.objects.get(usuario__pk=usuario.pk)
        controle = ControleDeCliente.objects.get(cliente__pk=cliente.pk)

    except:
        pass

    # os.getcwd()
    site = 'http://localhost:8000/'
    myhost = os.uname()[1]
    if myhost == 'ghabriel-pc':
        site = 'http://localhost:8000/'
        online = False
    if myhost == 'bernardo-Work':
        site = 'http://localhost:8000/'
        online = False
    elif myhost == 'MacBook-Pro.local':
        site = 'http://localhost:8000/'
        online = False
    elif myhost == 'venancio':
        site = 'http://localhost:8000/'
        online = False
    elif myhost == 'leandro-pc':
        site = 'http://localhost:8000/'
        online = False
    elif myhost =='web7641.kinghost.net':
        site = 'https://4maos.com.br/quatromaos/'

    return {'site':site, 'cliente':cliente, 'totalOportunidadesAtivas':totalOportunidadesAtivas, 'totalOportunidadesPagas':totalOportunidadesPagas, 'totalOportunidadesDisfarcadas':totalOportunidadesDisfarcadas, 'necessidadeForm':necessidadeForm, 'online':online, 'usuario': usuario, 'MEDIA_URL':settings.MEDIA_URL, 'MEDIA_ROOT': settings.MEDIA_ROOT, 'controle':controle}
