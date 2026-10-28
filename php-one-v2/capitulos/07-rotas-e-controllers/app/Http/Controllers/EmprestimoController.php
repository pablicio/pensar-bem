public function store(
    RegistrarEmprestimoRequest $request,
    RegistroDeEmprestimo $emprestimos,
) {
    $emprestimo = $emprestimos->registrar(
        exemplarId: $request->integer('exemplar_id'),
        leitorId: $request->integer('leitor_id'),
    );

    return response()
        ->json($emprestimo, 201)
        ->header('Location', route('emprestimos.show', $emprestimo));
}
