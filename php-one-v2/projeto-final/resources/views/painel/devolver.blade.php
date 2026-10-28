<x-layout titulo="Devolver">
    <form method="POST" action="{{ route('painel.devolver') }}">
        @csrf

        <label for="tombo">Tombo</label>
        <input id="tombo" name="tombo" value="{{ old('tombo') }}"
               autofocus>

        @error('tombo')
            <p class="erro">{{ $message }}</p>
        @enderror

        <label for="estado">Estado na volta</label>
        <select id="estado" name="estado">
            @foreach ($estados as $estado)
                <option value="{{ $estado->value }}"
                    @selected(old('estado') === $estado->value)>
                    {{ $estado->rotulo() }}
                </option>
            @endforeach
        </select>

        <button>Devolver</button>
    </form>
</x-layout>
