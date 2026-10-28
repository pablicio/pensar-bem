public function index(ListarLivrosRequest $request)
{
    $filtro = $request->filtro();

    $livros = Livro::filtrar($filtro)
        ->with('autores')
        ->paginate($filtro->porPagina)
        ->withQueryString();

    return LivroResource::collection($livros);
}
