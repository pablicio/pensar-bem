<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <title>{{ $titulo ?? 'Casa Amarela' }}</title>
</head>
<body>
    <header>
        <strong>Biblioteca Casa Amarela</strong>
        <nav>
            <a href="{{ route('painel.index') }}">Empréstimos</a>
            <a href="{{ route('painel.acervo') }}">Acervo</a>
        </nav>
    </header>

    <main>
        {{ $slot }}
    </main>
</body>
</html>
