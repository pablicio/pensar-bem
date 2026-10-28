public function store(StoreLivroRequest $request)
{
    $livro = Livro::create($request->validated());

    return response()
        ->json($livro, 201)
        ->header('Location', route('livros.show', $livro));
}
