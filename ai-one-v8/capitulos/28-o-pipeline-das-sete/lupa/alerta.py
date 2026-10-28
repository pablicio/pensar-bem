"""Às sete da manhã: do diário do dia aos alertas."""
import time

import torch

from .ajuste import Classificador, preve, tensores
from .bert import BERT
from .etiquetas import ROTULOS, Etiquetador, trechos_bio
from .etiquetas import tensores as tensores_bio
from .etiquetas import tokens_e_posicoes


class Lupa:
    def __init__(self, tok):
        V = len(tok.vocab)
        self.tok = tok
        self.relevancia = Classificador(BERT(V))
        self.etiquetador = Etiquetador(BERT(V))
        pesos = [(self.relevancia, "relevancia.pt"),
                 (self.etiquetador, "etiquetas.pt")]
        for modelo, arquivo in pesos:
            modelo.load_state_dict(torch.load(arquivo))
        self.relevancia.eval()
        self.etiquetador.eval()
        self.tempo = {"relevância": 0.0, "entidades": 0.0}

    @torch.no_grad()
    def entidades(self, texto):
        """Os trechos que o etiquetador marca, em texto."""
        ids, _ = tokens_e_posicoes(self.tok, texto)
        x, vazio, _ = tensores_bio([(ids, ["O"] * len(ids))],
                                   len(self.tok.vocab))
        palpite = self.etiquetador(x, vazio).argmax(-1)[0, 1:]
        rotulos = [ROTULOS[i] for i in palpite[:len(ids)]]
        return {nome: self.tok.decodifica(ids[a:b]).strip()
                for nome, a, b in trechos_bio(rotulos)}

    def dia(self, atos):
        """Os alertas de um dia: os atos relevantes, com o que
        foi possível tirar de cada um."""
        inicio = time.time()
        textos = [a["texto"] for a in atos]
        ids, vazio = tensores(textos, self.tok)
        relevante = preve(self.relevancia, ids, vazio)
        self.tempo["relevância"] += time.time() - inicio
        inicio = time.time()
        alertas = [dict(a, **self.entidades(a["texto"]))
                   for a, r in zip(atos, relevante) if r == 1]
        self.tempo["entidades"] += time.time() - inicio
        return alertas
