Schedule::call(function () {
    Emprestimo::emAberto()
        ->whereDate('devolver_ate', today()->addDay())
        ->pluck('id')
        ->each(fn ($id) => AvisarDevolucaoProxima::dispatch($id));
})->dailyAt('09:00')->name('avisos-de-devolucao');
