<?php

declare(strict_types=1);

namespace CasaAmarela\Emprestimos;

final class Dinheiro
{
    private function __construct(
        public readonly int $centavos,
    ) {
        if ($centavos < 0) {
            throw new \InvalidArgumentException('Valor negativo');
        }
    }

    public static function emCentavos(int $centavos): self
    {
        return new self($centavos);
    }

    public static function zero(): self
    {
        return new self(0);
    }

    public function mais(self $outro): self
    {
        return new self($this->centavos + $outro->centavos);
    }

    public function vezes(int $fator): self
    {
        return new self($this->centavos * $fator);
    }

    public function formatado(): string
    {
        $reais = $this->centavos / 100;

        return 'R$ ' . number_format($reais, 2, ',', '.');
    }
}
