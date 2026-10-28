public function attributes(): array
{
    return [
        'titulo' => 'título',
        'isbn' => 'ISBN',
    ];
}

public function messages(): array
{
    return [
        'isbn.unique' => 'Este ISBN já está no acervo.',
    ];
}
