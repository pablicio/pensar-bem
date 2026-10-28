public function __invoke(Request $request, Livro $livro)
{
    $request->validate([
        'capa' => ['required', 'image', 'max:2048'],
    ]);

    $caminho = $request->file('capa')->store('capas', 'public');

    $livro->update(['capa' => $caminho]);

    return response()->json(['capa' => $caminho], 201);
}
