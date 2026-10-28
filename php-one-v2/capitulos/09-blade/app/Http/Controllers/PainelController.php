public function emprestar(
    Request $request,
    RegistroDeEmprestimo $emprestimos,
) {
    $dados = $request->validate([
        'tombo' => ['required', 'integer'],
        'documento' => ['required', 'string'],
    ]);

    try {
        $emprestimos->registrarPorTombo(
            $dados['tombo'],
            $dados['documento'],
        );
    } catch (ExemplarIndisponivel $e) {
        return back()
            ->withInput()
            ->withErrors(['tombo' => $e->getMessage()]);
    }

    return redirect()
        ->route('painel.emprestar')
        ->with('sucesso', 'Emprestado.');
}
