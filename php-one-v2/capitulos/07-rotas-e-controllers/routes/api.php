Route::get('livros', [LivroController::class, 'index'])
    ->name('livros.index');

Route::post(
    'leitores/{leitor}/renovacoes',
    RenovacaoController::class,
)->whereNumber('leitor')->name('leitores.renovacoes');

Route::get('leitores/{leitor}/emprestimos', [
    EmprestimoController::class, 'porLeitor',
])->whereNumber('leitor')->name('leitores.emprestimos');
