public function update(Request $request, Livro $livro)
{
    $regras = [
        'titulo' => ['string', 'max:200'],
        'autor' => ['string', 'max:150'],
        'assunto' => ['string', 'max:40'],
        'isbn' => ['nullable', 'string', 'size:13'],
        'ano' => ['nullable', 'integer', 'min:1400'],
    ];

    if ($request->isMethod('PUT')) {
        $regras['titulo'][] = 'required';
        $regras['autor'][] = 'required';
        $regras['assunto'][] = 'required';
    }

    $livro->update($request->validate($regras));

    return $livro;
}
