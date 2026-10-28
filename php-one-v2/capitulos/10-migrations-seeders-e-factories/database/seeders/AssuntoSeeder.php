<?php

declare(strict_types=1);

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class AssuntoSeeder extends Seeder
{
    public function run(): void
    {
        $assuntos = [
            'literatura', 'didatico', 'infantil',
            'referencia', 'historia', 'ciencias',
        ];

        foreach ($assuntos as $nome) {
            DB::table('assuntos')->updateOrInsert(['nome' => $nome]);
        }
    }
}
