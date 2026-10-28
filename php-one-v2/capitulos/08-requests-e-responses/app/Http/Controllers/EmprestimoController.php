public function store(
    Request $request,
    RegistroDeEmprestimo $emprestimos,
) {
    $dados = $request->validate([
        'exemplar_id' => ['required', 'integer'],
        'leitor_id' => ['required', 'integer'],
    ]);

    $emprestimo = $emprestimos->registrar(
        exemplarId: $dados['exemplar_id'],
        leitorId: $dados['leitor_id'],
    );

    return response()
        ->json($emprestimo, 201)
        ->header(
            'Location',
            route('emprestimos.show', $emprestimo),
        );
}
