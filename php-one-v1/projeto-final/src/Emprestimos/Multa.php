<?php

namespace CasaAmarela\Emprestimos;

class Multa
{
    public function __construct(
        private int $centavos,
        public readonly int $diasDeAtraso,
    ) {
        if ($diasDeAtraso < 0) {
            throw new \InvalidArgumentException(
                "Dias de atraso negativos: {$diasDeAtraso}"
            );
        }

        if ($centavos < 0) {
            throw new \InvalidArgumentException(
                "Multa negativa: {$centavos}"
            );
        }
    }

    public function centavos(): int
    {
        return $this->centavos;
    }

    public function valorFormatado(): string
    {
        $reais = $this->centavos / 100;

        return 'R$ ' . number_format($reais, 2, ',', '.');
    }

    public function perdoar(): void
    {
        $this->centavos = 0;
    }
}
