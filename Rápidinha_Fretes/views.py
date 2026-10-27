from django.shortcuts import render, redirect
from .models import Manutencao, Veiculo


def home(request):
    return render(request, 'home.html')


def cadastrar(request):
    if request.method == 'POST':
        return redirect('home')

    return render(request, 'cadastrar.html')


def financeiro(request):

    if request.method == 'POST':

        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        veiculo_id = request.POST.get('veiculo')

        Manutencao.objects.create(
            tipo=tipo,
            descricao=descricao,
            custo=valor,
            data_entrada=data,
            id_veiculo_id=veiculo_id if veiculo_id else None
        )

        return redirect('financeiro')

    manutencoes = Manutencao.objects.all()

    total_manutencao = sum(
        manutencao.custo for manutencao in manutencoes
    )

    veiculos = Veiculo.objects.all()

    return render(
        request,
        'financeiro.html',
        {
            'manutencoes': manutencoes,
            'total_manutencao': total_manutencao,
            'veiculos': veiculos,
        }
    )


def veiculos(request):
    return render(request, 'veiculos.html')