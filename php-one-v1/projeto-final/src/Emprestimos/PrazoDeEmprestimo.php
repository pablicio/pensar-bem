<?php

declare(strict_types=1);

namespace CasaAmarela\Emprestimos;

final class PrazoDeEmprestimo
{
    public readonly \DateTimeImmutable $devolverAte;

    public function __construct(
        public readonly \DateTimeImmutable $retirada,
        public readonly int $dias,
    ) {
        if ($dias < 1) {
            throw new \InvalidArgumentException('Prazo inválido');
        }

        $this->devolverAte = $retirada->add(
            new \DateInterval("P{$dias}D")
        );
    }

    public function atrasadoEm(\DateTimeImmutable $quando): bool
    {
        return $quando > $this->devolverAte;
    }

    public function diasDeAtraso(\DateTimeImmutable $quando): int
    {
        if (!$this->atrasadoEm($quando)) {
            return 0;
        }

        return $this->devolverAte->diff($quando)->days;
    }
}
