<?php

namespace CasaAmarela\Circulacao;

trait RegistraHistorico
{
    private array $historico = [];

    public function registrar(string $evento): void
    {
        $this->historico[] = date('Y-m-d H:i:s') . ' ' . $evento;
    }

    public function historico(): array
    {
        return $this->historico;
    }
}
