public function store(
    RealizarEmprestimoRequest $request,
    EmprestimoService $emprestimos,
) {
    $emprestimo = $emprestimos->realizar(
        $request->integer('exemplar_id'),
        $request->integer('leitor_id'),
    );

    return (new EmprestimoResource($emprestimo))
        ->response()
        ->setStatusCode(201)
        ->header(
            'Location',
            route('emprestimos.show', $emprestimo),
        );
}
