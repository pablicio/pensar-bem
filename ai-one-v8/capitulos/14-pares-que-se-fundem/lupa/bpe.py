"""BPE sobre bytes, do zero."""
from collections import Counter


def pares(ids):
    """Quantas vezes cada par vizinho aparece."""
    return Counter(zip(ids, ids[1:]))


def funde(ids, par, novo):
    """Troca cada ocorrência de par pelo token novo."""
    saida, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and (ids[i], ids[i + 1]) == par:
            saida.append(novo)
            i += 2
        else:
            saida.append(ids[i])
            i += 1
    return saida


class BPE:
    def __init__(self):
        self.fusoes = {}                     # (a, b) -> novo
        self.vocab = {i: bytes([i]) for i in range(256)}

    def treina(self, texto, V):
        ids = list(texto.encode("utf-8"))
        for novo in range(256, V):
            contagem = pares(ids)
            par = max(contagem, key=contagem.get)
            ids = funde(ids, par, novo)
            self.fusoes[par] = novo
            a, b = par
            self.vocab[novo] = self.vocab[a] + self.vocab[b]
        return ids

    def codifica(self, texto):
        ids = list(texto.encode("utf-8"))
        while len(ids) >= 2:
            # o par que foi fundido primeiro no treino
            par = min(pares(ids), key=self.ordem)
            if par not in self.fusoes:
                break
            ids = funde(ids, par, self.fusoes[par])
        return ids

    def ordem(self, par):
        return self.fusoes.get(par, float("inf"))

    def decodifica(self, ids):
        b = b"".join(self.vocab[i] for i in ids)
        return b.decode("utf-8", errors="replace")

    def mostra(self, i):
        """O token i como texto legível, com · no espaço."""
        texto = self.vocab[i].decode("utf-8", "replace")
        return repr(texto)[1:-1].replace(" ", "·")
