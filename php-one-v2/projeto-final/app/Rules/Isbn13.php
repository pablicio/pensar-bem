<?php

declare(strict_types=1);

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Isbn13 implements ValidationRule
{
    public function validate(
        string $atributo,
        mixed $valor,
        Closure $falhar,
    ): void {
        if (!preg_match('/^\d{13}$/', (string) $valor)) {
            $falhar('O :attribute precisa ter 13 dígitos.');
            return;
        }

        $soma = 0;

        foreach (str_split(substr($valor, 0, 12)) as $i => $d) {
            $soma += (int) $d * ($i % 2 === 0 ? 1 : 3);
        }

        $verificador = (10 - $soma % 10) % 10;

        if ($verificador !== (int) $valor[12]) {
            $falhar('O :attribute não é um ISBN válido.');
        }
    }
}
