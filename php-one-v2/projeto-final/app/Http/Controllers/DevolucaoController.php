<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Models\Emprestimo;
use App\Services\RegistroDeDevolucao;
use Illuminate\Http\Request;

class DevolucaoController extends Controller
{
    public function __construct(
        private readonly RegistroDeDevolucao $devolucoes,
    ) {}

    public function __invoke(Request $req, Emprestimo $emprestimo)
    {
        $this->devolucoes->registrar(
            $emprestimo,
            $req->string('estado', 'bom')->toString(),
        );

        return response()->noContent();
    }
}
