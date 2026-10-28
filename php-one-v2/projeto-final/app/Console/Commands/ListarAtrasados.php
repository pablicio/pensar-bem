<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Services\ConsultaDeAtrasos;
use Illuminate\Console\Command;

class ListarAtrasados extends Command
{
    protected $signature = 'biblioteca:atrasados {--leitor=}';

    protected $description = 'Lista os vencidos em aberto';

    public function handle(ConsultaDeAtrasos $consulta): int
    {
        $leitor = $this->option('leitor');

        $linhas = $consulta->emAberto(
            $leitor === null ? null : (int) $leitor,
        );

        if ($linhas === []) {
            $this->info('Nenhum atrasado.');

            return self::SUCCESS;
        }

        $this->table(
            ['Tombo', 'Título', 'Leitor', 'Dias'],
            $linhas,
        );

        return self::FAILURE;
    }
}
