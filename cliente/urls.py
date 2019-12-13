from django.urls import path
from . import views

urlpatterns = [
    path('', views.oportunidades, name='oportunidades'),
    path('oportunidades/', views.oportunidades, name='oportunidades'),
    path('oportunidades-disfarcadas/', views.oportunidades_disfarcadas, name='oportunidades_disfarcadas'),
    path('oportunidade/<int:pk>/', views.oportunidade_detail, name='oportunidade_detail'),
    path('oportunidade-falar/<int:pk>/', views.oportunidade_falar, name='oportunidade_falar'),
    path('oportunidade/new', views.oportunidade_new, name='oportunidade_new'),
    path('oportunidade/<int:pk>/edit/', views.oportunidade_edit, name='oportunidade_edit'),

    path('servico/<link>/', views.servico_detail, name='servico_detail'),

    path('planos/', views.planos, name='planos'),
    # path('firstprofile/', views.firstprofile, name='firstprofile'),
    path('cronjob/', views.cronjob, name='cronjob'),


    path('material-marketing-apoio/', views.material_marketing_apoio, name='material_marketing_apoio'),
    path('material-marketing-avancado/', views.material_marketing_avancado, name='material_marketing_avancado'),
    path('conteudo-educativo/', views.conteudo_educativo, name='conteudo_educativo'),
    path('perfil/', views.perfil, name='perfil'),
    path('crop-logo/', views.crop_logo, name='crop_logo'),
    path('salvar-logo/', views.salvar_logo, name='salvar_logo'),
    path('duvidas-frequentes/', views.duvidas_frequentes, name='duvidas_frequentes'),
    path('logout/', views.logout, name='logout'),
]
