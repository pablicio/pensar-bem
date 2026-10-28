<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Models\Livro;

class LivroController extends Controller
{
    public function index()
    {
        return Livro::query()->orderBy('titulo')->paginate(20);
    }

    public function show(Livro $livro)
    {
        return $livro;
    }
}
