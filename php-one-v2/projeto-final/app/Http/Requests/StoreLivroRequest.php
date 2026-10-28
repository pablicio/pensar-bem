<?php

declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreLivroRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'titulo' => ['required', 'string', 'max:200'],
            'autor' => ['required', 'string', 'max:150'],
            'assunto' => ['required', 'string', 'max:40'],
            'isbn' => [
                'nullable', 'digits:13', 'unique:livros,isbn',
            ],
            'ano' => [
                'nullable', 'integer', 'min:1400',
                'max:' . now()->year,
            ],
        ];
    }
}
