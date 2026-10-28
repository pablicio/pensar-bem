public function index()
{
    $livros = Livro::orderBy('titulo')->paginate(20);

    return LivroResource::collection($livros);
}
