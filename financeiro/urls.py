from django.urls import path
from . import views as financeiro_views
from Rápidinha_Fretes import views as rapidinha_views

urlpatterns = [
    path("", financeiro_views.financeiro, name="financeiro"),
    path(
        "painel-admin/",
        rapidinha_views.painel_admin,
        name="painel_admin",
    ),
]