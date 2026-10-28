<h1>Empréstimos em aberto</h1>

<table>
    @forelse ($emprestimos as $emprestimo)
        <tr>
            <td>{{ $emprestimo->exemplar->tombo }}</td>
            <td>{{ $emprestimo->exemplar->livro->titulo }}</td>
            <td>{{ $emprestimo->leitor->nome }}</td>
            <td>{{ $emprestimo->devolver_ate->format('d/m/Y') }}</td>
        </tr>
    @empty
        <tr><td colspan="4">Nada emprestado agora.</td></tr>
    @endforelse
</table>
