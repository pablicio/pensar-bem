"""O registro de cada leitura, para refazê-la depois."""
import hashlib
import json

import torch

from leitora.decide import TEMPERATURA
from leitora.recorte import caixa, como_mnist, em_branco


def resumo(dados):
    """Os 16 primeiros algarismos do SHA-256."""
    return hashlib.sha256(dados).hexdigest()[:16]


def versao(modelo):
    """A impressão digital dos pesos, não a do arquivo."""
    pesos = b"".join(v.numpy().tobytes()
                     for v in modelo.state_dict().values())
    return resumo(pesos)


@torch.no_grad()
def le_caixas(modelo, folha, questao):
    """As entradas e os logitos de cada caixa escrita."""
    torch.set_num_threads(1)        # a conta, sempre igual
    caixas = []
    for k in range(3):
        tinta = caixa(folha, questao, k)
        if em_branco(tinta):
            caixas.append(None)
            continue
        x = como_mnist(tinta)
        z = modelo(torch.from_numpy(x)[None])[0]
        caixas.append({"entrada": resumo(x.tobytes()),
                       "logitos": z.tolist()})
    return caixas


def registra(arquivo, inscricao, questao, folha, modelo, lim):
    """Lê uma resposta e grava tudo o que a decidiu."""
    caixas = le_caixas(modelo, folha, questao)
    texto, confianca = "", 1.0
    for c in caixas:
        if c is None:
            texto += " "
            continue
        z = torch.tensor(c["logitos"])
        p = (z / TEMPERATURA).softmax(0)
        texto += str(int(p.argmax()))
        confianca *= p.max().item()
    numero = texto.lstrip()
    valida = " " not in numero
    r = {"inscricao": int(inscricao), "questao": questao + 1,
         "cartao": resumo(folha.tobytes()),
         "modelo": versao(modelo), "temperatura": TEMPERATURA,
         "limiar": lim, "caixas": caixas, "texto": texto,
         "lido": int(numero) if numero and valida else None,
         "confianca": confianca,
         "destino": "leitora" if valida and confianca >= lim
         else "revisão"}
    arquivo.write(json.dumps(r, ensure_ascii=False) + "\n")
    return r


def rele(registro, folha, modelo):
    """Refaz a leitura e diz se deu exatamente a mesma."""
    if versao(modelo) != registro["modelo"]:
        return "recusada: outra leitora"
    if resumo(folha.tobytes()) != registro["cartao"]:
        return "recusada: outro cartão"
    q = registro["questao"] - 1
    if le_caixas(modelo, folha, q) == registro["caixas"]:
        return "idêntica, bit a bit"
    return "DIFERENTE"
