"""Ler o que um pickle importaria, sem carregá-lo."""
import pickletools

# o que um modelo do scikit-learn costuma precisar
ESPERADOS = {"sklearn", "numpy", "scipy"}
AVULSOS = {"builtins.slice", "functools.partial"}


def importados(dados):
    """Os nomes que o pickle pede para importar."""
    memo, recentes, nomes = [], [], set()
    for op, arg, _ in pickletools.genops(dados):
        if isinstance(arg, str):
            recentes.append(arg)
        elif op.name in ("BINGET", "LONG_BINGET"):
            recentes.append(memo[arg])
        if op.name == "MEMOIZE":
            memo.append(recentes[-1] if recentes else None)
        if op.name == "STACK_GLOBAL":
            nomes.add(".".join(recentes[-2:]))
        elif op.name == "GLOBAL":
            nomes.add(arg.replace(" ", "."))
    return nomes


def fora_do_esperado(nomes):
    """Os nomes que não são do que um modelo costuma usar."""
    return sorted(n for n in nomes if n not in AVULSOS
                  and n.split(".")[0] not in ESPERADOS)
