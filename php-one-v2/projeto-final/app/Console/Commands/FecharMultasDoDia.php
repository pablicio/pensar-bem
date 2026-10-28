<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Services\CalculadoraDeMultas;
use Illuminate\Console\Command;

class FecharMultasDoDia extends Command
{
    protected $signature = 'biblioteca:multas {--data=}';

    protected $description = 'Calcula as multas dos vencidos';

    public function handle(CalculadoraDeMultas $calculadora): int
    {
        $data = $this->option('data') ?? now()->toDateString();

        $resultado = $calculadora->fecharDia($data);

        $this->info("Dia {$data}: {$resultado->quantidade} multas");
        $this->info("Total: {$resultado->total->formatado()}");

        return self::SUCCESS;
    }
}
