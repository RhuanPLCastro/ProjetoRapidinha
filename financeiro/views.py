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
            id_veiculo_id=veiculo_id
        )

        return redirect('financeiro')

    manutencoes = Manutencao.objects.all()
    veiculos = Veiculo.objects.all()

    total_manutencao = sum(
        manutencao.custo for manutencao in manutencoes
    )

    return render(
        request,
        'financeiro.html',
        {
            'manutencoes': manutencoes,
            'total_manutencao': total_manutencao,
            'veiculos': veiculos,
        }
    )