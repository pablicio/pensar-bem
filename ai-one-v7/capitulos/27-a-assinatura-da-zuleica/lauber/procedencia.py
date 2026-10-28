"""O registro de procedência de cada estampa da coleção."""
import hashlib
import json

import numpy as np

from lauber.vizinhos import normaliza


def impressao(caminho):
    """Os 16 primeiros dígitos do SHA-256 de um arquivo: mudam
    se um único byte do arquivo mudar."""
    with open(caminho, "rb") as arquivo:
        return hashlib.sha256(arquivo.read()).hexdigest()[:16]


def parecidas(estampa, base, info, indices, k=3):
    """As k estampas da base mais parecidas com a estampa (com
    espelho), com o ano e se são da Zuleica."""
    b = normaliza(base)
    s = np.maximum(normaliza(estampa) @ b.T,
                   normaliza(estampa.flip(3)) @ b.T)[0]
    melhores = np.argsort(-s)[:k]
    return [{"acervo": int(indices[j]),
             "ano": int(info["ano"][indices[j]]),
             "zuleica": bool(info["zuleica"][indices[j]]),
             "correlacao": round(float(s[j]), 3)}
            for j in melhores]


def registro(numero, maquina, verificacoes, vizinhas):
    """Tudo o que se sabe sobre como a estampa foi feita, mais
    os campos que só a desenhista preenche."""
    return {"estampa": numero,
            "maquina": maquina,
            "verificacoes": verificacoes,
            "parecidas_no_acervo": vizinhas,
            "pessoa": {"escolhida_por": None,
                       "alteracoes": None,
                       "assinatura": None}}


def grava(registros, caminho):
    """Uma linha de JSON por estampa."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for r in registros:
            linha = json.dumps(r, ensure_ascii=False)
            arquivo.write(linha + "\n")
