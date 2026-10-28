public function index(ListarEmprestimosRequest $request)
{
    $emprestimos = Emprestimo::visivelPara($request->user())
        ->when(
            $request->filled('leitor_id'),
            fn ($q) => $q->where(
                'leitor_id',
                $request->integer('leitor_id'),
            ),
        )
        ->with('exemplar.livro')
        ->orderByDesc('retirado_em')
        ->orderByDesc('id')
        ->cursorPaginate(20);

    return EmprestimoResource::collection($emprestimos);
}
