from django.shortcuts import render
from django.db.models import Sum
from .models import Veiculo, Manutencao, Motorista


def home(request):
    return render(request, 'home.html')

def dashboard(request):
    veiculos = Veiculo.objects.all()
    veiculos_ociosos = veiculos.filter(status="Ativo").count()
    total_motoristas = Motorista.objects.count()
    gastos_totais = Manutencao.objects.aggregate(total=Sum('custo'))['total'] or 0
    manutencoes = Manutencao.objects.all().order_by('-data_entrada')

    contexto = {
        'veiculos': veiculos,
        'veiculos_ociosos': veiculos_ociosos,
        'total_motoristas': total_motoristas,
        'gastos_totais': gastos_totais,
        'manutencoes': manutencoes,
    }

    return render(request, 'home.html', contexto)
