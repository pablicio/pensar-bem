public function __invoke(Request $request, Emprestimo $emprestimo)
{
    $estado = $request->enum('estado', StatusExemplar::class)
        ?? StatusExemplar::Bom;

    $this->devolucoes->registrar($emprestimo, $estado);

    return response()->noContent();
}
