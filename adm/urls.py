from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_cadastro_clientes, name='admin_cadastro_clientes'),
    path('cadastro-clientes/', views.admin_cadastro_clientes, name='admin_cadastro_clientes'),
    path('cliente/<int:pk>/edit/', views.admin_cliente_edit, name='admin_cliente_edit'),
    path('controle-acesso/', views.admin_controle_acesso, name='admin_controle_acesso'),
    path('gestao-oportunidades/', views.admin_gestao_oportunidades, name='admin_gestao_oportunidades'),
    path('upload-oportunidades/', views.admin_upload_oportunidades, name='admin_upload_oportunidades'),
    path('upload-oportunidades-disfarcadas/', views.admin_upload_oportunidades_disfarcadas, name='admin_upload_oportunidades_disfarcadas'),
    path('upload-conteudo-educativo/', views.admin_conteudo_educativo, name='admin_conteudo_educativo'),
    path('upload-marketing-apoio/', views.admin_upload_marketing_apoio, name='admin_upload_marketing_apoio'),
    path('upload-marketing-avancado/', views.admin_upload_marketing_avancado, name='admin_upload_marketing_avancado'),
    path('export/csv/', views.exportar_clientes_csv, name='exportar_clientes_csv'),
]
