"""Os diários em tokens, para os modelos de linguagem."""
import torch

from lupa.diario import atos
from lupa.tokenizador import Tokenizador


def prepara(V=2000):
    """O tokenizador e os tokens de 2026 (treino) e de 2027."""
    corpus = atos()
    treino = [a["texto"] for a in corpus if a["data"] < "2027"]
    teste = [a["texto"] for a in corpus if a["data"] >= "2027"]
    tok = Tokenizador()
    tok.treina(treino, V)

    def ids(textos):
        # cada ato termina com <|fim|>
        todos = [i for t in textos
                 for i in tok.codifica(t + "<|fim|>")]
        return torch.tensor(todos)

    return tok, ids(treino), ids(teste)
