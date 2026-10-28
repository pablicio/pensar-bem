$emprestimo = DB::transaction(function () use (/* ... */) {
    // ... as conferências e a gravação ...

    EmprestimoRealizado::dispatch($emprestimo);

    return $emprestimo;
});
