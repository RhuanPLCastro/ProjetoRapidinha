from django.contrib import admin
from django.urls import path
from Rápidinha_Fretes import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.cadastrar, name='inicio'),
    path('home/', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),

    path('financeiro/', views.financeiro, name='financeiro'),

    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/posicao/<str:placa>/', views.posicao_veiculo, name='posicao_veiculo'),

    path('painel-admin/', views.painel_admin, name='painel_admin'),
    path('sair/', views.sair, name='sair'),
]