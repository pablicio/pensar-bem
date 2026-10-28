@props(['acao', 'rotulo' => 'Tombo', 'valor' => null])

<form method="GET" action="{{ $acao }}" class="busca">
    <label for="tombo">{{ $rotulo }}</label>
    <input id="tombo" name="tombo"
           value="{{ $valor ?? request('tombo') }}" autofocus>
    <button>Buscar</button>
</form>
