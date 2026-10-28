public function store(Request $request)
{
    $dados = $request->validate([
        'exemplar_id' => [
            'required', 'integer', 'exists:exemplares,id',
        ],
        'leitor_id' => [
            'required', 'integer', 'exists:leitores,id',
        ],
    ]);

    $emprestimo = DB::transaction(function () use ($dados) {
        $exemplar = Exemplar::lockForUpdate()
            ->findOrFail($dados['exemplar_id']);

        if ($exemplar->estado !== StatusExemplar::Bom) {
            abort(409, 'Exemplar indisponível');
        }

        $abertos = Emprestimo::emAberto()
            ->where('leitor_id', $dados['leitor_id'])
            ->count();

        if ($abertos >= config('biblioteca.limite_por_leitor')) {
            abort(409, 'Limite de empréstimos atingido');
        }

        $emprestimo = Emprestimo::create([
            'exemplar_id' => $exemplar->id,
            'leitor_id' => $dados['leitor_id'],
            'retirado_em' => now(),
            'devolver_ate' => now()->addDays(
                config('biblioteca.prazo_em_dias'),
            ),
        ]);

        $exemplar->update(['estado' => StatusExemplar::Emprestado]);

        return $emprestimo;
    });

    return response()
        ->json($emprestimo, 201)
        ->header('Location', route('emprestimos.show', $emprestimo));
}
