from django.contrib import admin
from .models import LivrosArtigos, Categoria, Videos, Blog, MaterialDeApoioBasico, ListaDeServicosDoFiltroDeOportunidades, Cidade, TipoDeEmpresa, MaterialDeMarketingAvancado, Galeria, Arquivo, Oportunidade, LinksDoMenu, Servico, TipoDeCliente, Plano, TratativasDeOportunidades, DuvidasSobreOportunidades, Necessidades, DuvidasFrequentes, ConteudoEducativo

class ServicoAdmin(admin.ModelAdmin):
    list_display = ['autor','nome','valor','link','imagem','dataDeCadastro']
    prepopulated_fields = {'link':('nome',)}

class BlogAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sinopse','conteudo','capa','dataDeCadastro']


admin.site.register(Videos)
admin.site.register(Blog,BlogAdmin)
admin.site.register(LivrosArtigos)
admin.site.register(Plano)
admin.site.register(LinksDoMenu)
admin.site.register(Servico, ServicoAdmin)
admin.site.register(TipoDeCliente)
admin.site.register(Oportunidade)
admin.site.register(Cidade)
admin.site.register(Categoria)
admin.site.register(ListaDeServicosDoFiltroDeOportunidades)
# admin.site.register(TratativasDeOportunidades)
admin.site.register(DuvidasSobreOportunidades)
admin.site.register(Necessidades)
admin.site.register(DuvidasFrequentes)
admin.site.register(ConteudoEducativo)
admin.site.register(MaterialDeMarketingAvancado)
admin.site.register(MaterialDeApoioBasico)
admin.site.register(Galeria)
admin.site.register(Arquivo)
admin.site.register(TipoDeEmpresa)
