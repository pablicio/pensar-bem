<?php

declare(strict_types=1);

use App\Http\Controllers\DevolucaoController;
use App\Http\Controllers\EmprestimoController;
use App\Http\Controllers\ExemplarController;
use App\Http\Controllers\LivroController;
use Illuminate\Support\Facades\Route;

Route::apiResource('livros', LivroController::class);

Route::get('livros/{livro}/exemplares', [
    ExemplarController::class, 'porLivro',
])->name('livros.exemplares');

Route::post('emprestimos', [EmprestimoController::class, 'store'])
    ->name('emprestimos.store');

Route::post(
    'emprestimos/{emprestimo}/devolucao',
    DevolucaoController::class,
)->name('emprestimos.devolucao');
