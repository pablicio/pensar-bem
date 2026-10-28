public function renovar(
    int $emprestimoId,
    DateTimeImmutable $quando,
): Emprestimo {
    return DB::transaction(function () use (
        $emprestimoId, $quando,
    ) {
        $e = Emprestimo::with(['leitor', 'exemplar.livro'])
            ->lockForUpdate()
            ->findOrFail($emprestimoId);

        if ($e->devolvido()) {
            throw new EmprestimoJaDevolvido($e->id);
        }

        if ($e->emAtraso($quando)) {
            throw new RenovacaoDeAtrasado($e->id);
        }

        if ($e->renovacoes >= 2) {
            throw new RenovacaoEsgotada($e->id, 2);
        }

        if ($e->exemplar->livro->temReservaAtiva()) {
            throw new LivroReservado($e->exemplar->livro_id);
        }

        $dias = $this->regras->prazoPara($e->leitor);

        $e->renovarAte($quando->modify("+{$dias} days"));

        return $e;
    });
}
