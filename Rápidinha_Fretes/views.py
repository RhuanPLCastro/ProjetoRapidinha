from decimal import Decimal, InvalidOperation
from functools import wraps

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import Login, Manutencao, Veiculo

CARGOS = ('Funcionario', 'Administrador')


def apenas_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.session.get('cargo') != 'Administrador':
            return redirect('home')
        return view(request, *args, **kwargs)
    return wrapper


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
    return render(request, 'veiculos.html')