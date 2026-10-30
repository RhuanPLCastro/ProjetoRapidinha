from django.contrib import admin
from django.urls import path, include
from Rápidinha_Fretes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.cadastrar, name='inicio'),
    path('home/', views.home, name='home'), 
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('sair/', views.sair, name='sair'),
    
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculos/remover/<int:id_veiculo>/', views.remover_veiculo, name='remover_veiculo'),
    path('veiculos/status/<int:id_veiculo>/', views.alterar_status_veiculo, name='alterar_status_veiculo'),
    path('veiculos/posicao/<str:placa>/', views.posicao_veiculo, name='posicao_veiculo'),
    
    path('painel-admin/', views.painel_admin, name='painel_admin'),
    path('financeiro/', include('financeiro.urls')),
]