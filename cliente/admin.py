from django.contrib import admin
from .models import Cliente, ControleDeCliente, NegociacoesDeOportunidades, AreaDeAtuacao
# from import_export import resources

# class ClienteResource(resources.ModelResource):
#
#     class Meta:
#         model = Cliente
admin.site.register(AreaDeAtuacao)
admin.site.register(Cliente)
admin.site.register(ControleDeCliente)
admin.site.register(NegociacoesDeOportunidades)
