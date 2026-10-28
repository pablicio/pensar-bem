use Illuminate\Http\Request;

public function index(Request $request)
{
    $busca = $request->query('q');
    $pagina = $request->integer('pagina', 1);

    return Livro::buscar($busca)->paginate(20, page: $pagina);
}
