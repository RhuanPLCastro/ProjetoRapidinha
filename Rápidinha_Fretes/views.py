import math
from datetime import date
from decimal import Decimal, InvalidOperation
from functools import wraps

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from .models import Login, Manutencao, Veiculo


CARGOS = ('Funcionario', 'Mecanico', 'Administrador')

ORIGEM = ("São Paulo", -23.5505, -46.6333)
DESTINO = ("Campinas", -22.9099, -47.0626)

def apenas_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.session.get('cargo') != 'Administrador':
            messages.error(request, "Acesso negado: Apenas administradores.")
            return redirect('home')
        return view(request, *args, **kwargs)
    return wrapper

def admin_ou_mecanico(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        cargo = request.session.get('cargo')
        if cargo not in ['Administrador', 'Mecanico']:
            messages.error(request, "Acesso negado: Você não tem permissão para alterar o status.")
            return redirect('veiculos')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def iniciar_sessao(request, usuario):
    request.session.cycle_key()
    request.session['login_id'] = usuario.id_login
    request.session['usuario'] = usuario.usuario
    request.session['cargo'] = usuario.cargo

def home(request):
    return render(request, 'home.html')

def cadastrar(request):
    erro = None
    acao = None

    if request.method == 'POST':
        acao = request.POST.get('acao')
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')

        if acao == 'entrar':
            usuario = Login.objects.filter(usuario=email).first()
            if usuario and check_password(senha, usuario.senha):
                iniciar_sessao(request, usuario)
                return redirect('home')
            erro = 'E-mail ou senha incorretos.'
        else:
            acao = 'cadastrar'
            nome = request.POST.get('nome', '').strip()
            if not nome or not email or not senha:
                erro = 'Preencha todos os campos.'
            elif len(email) > 50:
                erro = 'E-mail muito longo (máximo de 50 caracteres).'
            elif Login.objects.filter(usuario=email).exists():
                erro = 'Esse e-mail já está cadastrado.'
            else:
                usuario = Login.objects.create(
                    usuario=email,
                    senha=make_password(senha),
                    cargo='Funcionario',
                )
                iniciar_sessao(request, usuario)
                return redirect('home')

    return render(request, 'cadastrar.html', {'erro': erro, 'acao': acao})

def sair(request):
    request.session.flush()
    return redirect('cadastrar')

@apenas_admin
def painel_admin(request):
    if request.method == 'POST':
        cargo = request.POST.get('cargo')
        if cargo in CARGOS:
            Login.objects.filter(
                id_login=request.POST.get('id_login')
            ).update(cargo=cargo)
        return redirect('painel_admin')

    return render(request, 'painel_admin.html', {
        'usuarios': Login.objects.all().order_by('usuario'),
        'cargos': CARGOS,
    })

def financeiro(request):
    erro = None
    if request.method == 'POST':
        try:
            manutencao = Manutencao(
                tipo=request.POST.get('tipo'),
                descricao=request.POST.get('descricao'),
                custo=Decimal(request.POST.get('valor')),
                data_entrada=request.POST.get('data'),
                id_veiculo_id=request.POST.get('veiculo') or None,
            )
            manutencao.full_clean()
            manutencao.save()
            return redirect('financeiro')
        except (ValidationError, InvalidOperation, TypeError):
            erro = 'Não foi possível salvar. Confira os campos e o veículo.'

    manutencoes = Manutencao.objects.select_related('id_veiculo').order_by('-data_entrada')
    return render(request, 'financeiro.html', {
        'manutencoes': manutencoes,
        'total_manutencao': manutencoes.aggregate(t=Sum('custo'))['t'] or 0,
        'veiculos': Veiculo.objects.all(),
        'erro': erro,
    })

def veiculos(request):
    lista_veiculos = Veiculo.objects.all()
    return render(request, 'veiculos.html', {'veiculos': lista_veiculos})

def distancia_km(lat1, lng1, lat2, lng2):
    raio = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2)
    return raio * 2 * math.asin(math.sqrt(a))

def buscar_posicao(placa):
    cabecalho = {"Authorization": "Bearer " + settings.RASTREIO_KEY}
    resposta = requests.get(settings.RASTREIO_URL + "/api/devices", params={"uniqueId": placa}, headers=cabecalho, timeout=5)
    resposta.raise_for_status()
    dispositivos = resposta.json()
    if not dispositivos:
        raise ValueError("Veículo não cadastrado no Traccar")
    resposta = requests.get(settings.RASTREIO_URL + "/api/positions", params={"deviceId": dispositivos[0]["id"]}, headers=cabecalho, timeout=5)
    resposta.raise_for_status()
    posicoes = resposta.json()
    if not posicoes:
        raise ValueError("Veículo ainda sem posição")
    return posicoes[0]["latitude"], posicoes[0]["longitude"]

def posicao_veiculo(request, placa):
    try:
        lat, lng = buscar_posicao(placa)
    except Exception:
        return JsonResponse({"erro": "Sem sinal do veículo"}, status=502)

    total = distancia_km(ORIGEM[1], ORIGEM[2], DESTINO[1], DESTINO[2])
    percorrido = distancia_km(ORIGEM[1], ORIGEM[2], lat, lng)
    progresso = min(100, round(percorrido / total * 100))
    return JsonResponse({
        "placa": placa, "lat": lat, "lng": lng, "origem": ORIGEM[0], "destino": DESTINO[0],
        "progresso": progresso, "restante_km": round(max(0, total - percorrido)),
    })

@apenas_admin
def adicionar_veiculo(request):
    if request.method == 'POST':
        Veiculo.objects.create(
            placa=request.POST.get('placa'),
            numero_frota=request.POST.get('numero_frota'),
            tipo=request.POST.get('tipo'),
            modelo=request.POST.get('modelo'),
            combustivel=request.POST.get('combustivel')
        )
        messages.success(request, "Veículo adicionado com sucesso!")
        return redirect('veiculos')
    return render(request, 'adicionar_veiculo.html')

@apenas_admin
def remover_veiculo(request, id_veiculo):
    veiculo = get_object_or_404(Veiculo, id_veiculo=id_veiculo)
    veiculo.delete()
    messages.success(request, "Veículo removido com sucesso!")
    return redirect('veiculos')

@admin_ou_mecanico
def alterar_status_veiculo(request, id_veiculo):
    veiculo = get_object_or_404(Veiculo, id_veiculo=id_veiculo)
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        
        if novo_status == 'Em Manutenção':
            descricao = request.POST.get('descricao_problema')
            custo = request.POST.get('custo') or 0
            
            Manutencao.objects.create(
                id_veiculo=veiculo,
                tipo='Corretiva',
                descricao=descricao,
                custo=custo,
                data_entrada=date.today()
            )
            veiculo.status = 'Em Manutenção'
        elif novo_status == 'Ativo':
            veiculo.status = 'Ativo'
            ultima_manutencao = Manutencao.objects.filter(id_veiculo=veiculo, data_saida__isnull=True).first()
            if ultima_manutencao:
                ultima_manutencao.data_saida = date.today()
                ultima_manutencao.save()

        veiculo.save()
        messages.success(request, f"Status do veículo {veiculo.placa} atualizado para {novo_status}.")
        return redirect('veiculos')
        
    return render(request, 'alterar_status.html', {'veiculo': veiculo})