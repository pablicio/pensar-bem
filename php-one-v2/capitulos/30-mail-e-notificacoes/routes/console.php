Schedule::call(function () {
    Emprestimo::emAberto()
        ->whereDate('devolver_ate', today()->addDay())
        ->with('leitor', 'exemplar.livro')
        ->each(fn (Emprestimo $e) => $e->leitor->notify(
            new DevolucaoAmanha($e),
        ));
})->dailyAt('09:00')->name('avisos-de-devolucao');
