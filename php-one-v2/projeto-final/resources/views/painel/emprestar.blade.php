<x-layout titulo="Emprestar">
    <form method="POST" action="{{ route('painel.emprestar') }}">
        @csrf

        <label for="tombo">Tombo</label>
        <input id="tombo" name="tombo" value="{{ old('tombo') }}"
               autofocus>

        @error('tombo')
            <p class="erro">{{ $message }}</p>
        @enderror

        <label for="documento">Documento do leitor</label>
        <input id="documento" name="documento"
               value="{{ old('documento') }}">

        @error('documento')
            <p class="erro">{{ $message }}</p>
        @enderror

        <button>Emprestar</button>
    </form>
</x-layout>
