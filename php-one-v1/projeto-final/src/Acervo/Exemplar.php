<?php

namespace CasaAmarela\Acervo;

class Exemplar
{
    private const ESTADOS = [
        'bom', 'emprestado', 'danificado', 'restauro', 'extraviado',
    ];

    public function __construct(
        public int $tombo,
        public Livro $livro,
        private string $estado = 'bom',
    ) {
        if ($tombo <= 0) {
            throw new \InvalidArgumentException(
                "Tombo inválido: {$tombo}"
            );
        }

        if (!in_array($estado, self::ESTADOS, true)) {
            throw new \InvalidArgumentException(
                "Estado desconhecido: {$estado}"
            );
        }
    }
}
