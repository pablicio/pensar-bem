<?php

declare(strict_types=1);

namespace CasaAmarela;

use Closure;
use RuntimeException;

final class Servicos
{
    /** @var array<string, Closure> */
    private array $fabricas = [];

    /** @var array<string, object> */
    private array $prontos = [];

    public function registrar(string $nome, Closure $fabrica): void
    {
        $this->fabricas[$nome] = $fabrica;
    }

    public function get(string $nome): object
    {
        if (!isset($this->fabricas[$nome])) {
            throw new RuntimeException("desconhecido: {$nome}");
        }
        $fabrica = $this->fabricas[$nome];
        return $this->prontos[$nome] ??= $fabrica($this);
    }
}
