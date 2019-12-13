from adm.models import Oportunidade, ListaDeServicosDoFiltroDeOportunidades, TipoDeCliente
from django import forms
import django_filters
from django.shortcuts import get_object_or_404

class OportunidadeFilter(django_filters.FilterSet):
    class Meta:
        model = Oportunidade
        fields = ['servicoSolicitado', 'tipoDeCliente', 'cidade', 'status' ]

    choices_status = (
        ('Aguardando publicação', 'Aguardando publicação'),
        ('Tentando contato', 'Tentando contato'),
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
    )

    if get_object_or_404(ListaDeServicosDoFiltroDeOportunidades):
        servicoSolicitado = django_filters.ModelMultipleChoiceFilter(
                queryset=get_object_or_404(ListaDeServicosDoFiltroDeOportunidades).servicosFiltraveis.all(), widget=forms.CheckboxSelectMultiple)
    tipoDeCliente = django_filters.ModelMultipleChoiceFilter(
            queryset=TipoDeCliente.objects.all(), widget=forms.CheckboxSelectMultiple)
    status = django_filters.ChoiceFilter(choices=choices_status,widget=forms.CheckboxSelectMultiple)
