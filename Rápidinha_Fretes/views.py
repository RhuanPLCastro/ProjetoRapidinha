from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def cadastrar(request):
    if request.method == 'POST':
        return redirect('home')

    return render(request, 'cadastrar.html')


def financeiro(request):
    return render(request, 'financeiro.html')


def veiculos(request):
    return render(request, 'veiculos.html')
