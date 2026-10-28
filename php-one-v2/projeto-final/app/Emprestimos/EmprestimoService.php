<?php

declare(strict_types=1);

namespace App\Emprestimos;

use App\Avisos\EnviadorDeAviso;
use App\Models\Emprestimo;
use App\Models\Exemplar;
use App\Models\Leitor;
use Illuminate\Support\Facades\DB;

final class EmprestimoService
{
    public function __construct(
        private readonly RegrasDeCirculacao $regras,
        private readonly EnviadorDeAviso $avisos,
    ) {}

    public function realizar(
        int $exemplarId,
        int $leitorId,
        ?Autorizacao $autorizacao = null,
    ): Emprestimo {
        $emprestimo = DB::transaction(function () use (
            $exemplarId, $leitorId, $autorizacao,
        ) {
            $exemplar = Exemplar::with('livro')
                ->lockForUpdate()
                ->findOrFail($exemplarId);

            $leitor = Leitor::lockForUpdate()
                ->findOrFail($leitorId);

            $this->exigirExemplarEmprestavel(
                $exemplar, $autorizacao,
            );
            $this->exigirLeitorEmDia($leitor);

            $prazo = $this->regras->prazoPara($leitor);

            $emprestimo = Emprestimo::create([
                'exemplar_id' => $exemplar->id,
                'leitor_id' => $leitor->id,
                'retirado_em' => now(),
                'devolver_ate' => now()->addDays($prazo),
                'autorizado_por' => $autorizacao?->usuarioId,
            ]);

            $exemplar->marcarEmprestado();

            return $emprestimo;
        });

        $this->avisos->enviar(
            $emprestimo->leitor,
            "Empréstimo feito. Devolva até "
                . $emprestimo->devolver_ate->format('d/m') . '.',
        );

        return $emprestimo;
    }

    // ...
}
