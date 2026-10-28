$livros = Livro::orderBy('titulo')->paginate(47);

foreach ($livros as $livro) {
    echo $livro->titulo;
    echo $livro->autores->pluck('nome')->join(', ');
    echo $livro->exemplares->count();
}
