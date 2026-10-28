"""A triagem: a média da LSTM e do Naive Bayes."""
import torch

from rio.bayes import Bayes
from rio.leitor import Leitor, preenche, probabilidades
from rio.texto import Vocabulario, mensagens, palavras, parte


def carrega(arquivo="leitor.pt"):
    """O vocabulário, a LSTM do capítulo 21 e o Naive Bayes."""
    treino = parte(mensagens(), "treino")
    voc = Vocabulario(treino["texto"], palavras)
    leitor = Leitor(len(voc))
    leitor.load_state_dict(torch.load(arquivo))
    bayes = Bayes(treino["texto"], treino["classe"])
    return voc, leitor, bayes


def triagem(textos, voc, leitor, bayes):
    """As quatro probabilidades de cada mensagem."""
    lstm = probabilidades(leitor, *preenche(voc, textos))
    return (lstm + bayes.probabilidades(textos)) / 2
