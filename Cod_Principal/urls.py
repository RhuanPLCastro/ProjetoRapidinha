from django.contrib import admin
from django.urls import path
from Rápidinha_Fretes import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.cadastrar, name='inicio'),
<<<<<<< HEAD
    path('home/', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),

    path('financeiro/', views.financeiro, name='financeiro'),

    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/posicao/<str:placa>/', views.posicao_veiculo, name='posicao_veiculo'),

    path('painel-admin/', views.painel_admin, name='painel_admin'),
    path('sair/', views.sair, name='sair'),
=======
    path('cadastrar/', views.cadastrar, name='cadastrar'),
<<<<<<< HEAD
    path('financeiro/', include('financeiro.urls')),
=======
    path('sair/', views.sair, name='sair'),

    path('home/', views.home, name='home'),
    path('financeiro/', views.financeiro, name='financeiro'),
>>>>>>> 687465b (Atualiza painel administrativo)
    path('veiculos/', views.veiculos, name='veiculos'),

    path('painel-admin/', views.painel_admin, name='painel_admin'),
>>>>>>> b531bb55163f504a25d71df33644fe4a6daf3725
]