<?php

declare(strict_types=1);

namespace App\Casts;

use App\Emprestimos\Dinheiro;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class DinheiroCast implements CastsAttributes
{
    public function get($model, $chave, $valor, $atributos): ?Dinheiro
    {
        return $valor === null
            ? null
            : Dinheiro::emCentavos((int) $valor);
    }

    public function set($model, $chave, $valor, $atributos): ?int
    {
        return $valor?->centavos;
    }
}
