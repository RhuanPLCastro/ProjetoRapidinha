<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from Rápidinha_Fretes import views

=======
"""
URL configuration for Cod_Principal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Rápidinha_Fretes import views


>>>>>>> b531bb55163f504a25d71df33644fe4a6daf3725
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