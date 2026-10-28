import re
import time

import torch
from sklearn.feature_extraction.text import TfidfVectorizer

from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos, gabarito
from lupa.extrator import limpa
from lupa.vetores import infonce, vetores

torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
OBJETO = re.compile(r"Objeto(?: do contrato)?: (.+?)\.\s")
categoria = {i: g["categoria"] for i, g in gabarito().items()}


def pares(lista):
    """(objeto, o ato sem o objeto, categoria) de cada ato."""
    saida = []
    for a in lista:
        t = limpa(a["texto"])
        m = OBJETO.search(t)
        if m:
            resto = t[:m.start(1)] + t[m.end(1):]
            c = categoria[a["id"]]
            saida.append((m.group(1), resto, c))
    return saida


corpus = atos()
treino = pares(a for a in corpus if a["data"] < "2027")
teste = pares(a for a in corpus if a["data"] >= "2027")
print(f"{len(treino)} pares de treino, {len(teste)} de teste")
objetos = [q for q, _, _ in teste]
restos = [d for _, d, _ in teste]
cats = [c for _, _, c in teste]
mesma = torch.tensor([[a == b for b in cats] for a in cats])
acaso = mesma.float().mean().item()
print(f"acaso: {acaso:.3f} dos atos são da mesma categoria")


def mede(nome, Q, D):
    """O próprio ato entre os 10 primeiros? E os 10 primeiros
    são da mesma categoria do objeto?"""
    notas = Q @ D.T
    posicao = (notas > notas.diagonal()[:, None]).sum(1) + 1
    r10 = (posicao <= 10).float().mean().item()
    top = notas.topk(10, dim=1).indices
    p10 = mesma.gather(1, top).float().mean().item()
    print(f"{nome:15} o próprio no top 10: {r10:.3f}"
          f"  categoria@10: {p10:.3f}")


tfidf = TfidfVectorizer(sublinear_tf=True).fit(restos)
Q_tfidf = torch.tensor(tfidf.transform(objetos).toarray())
D_tfidf = torch.tensor(tfidf.transform(restos).toarray())
mede("TF-IDF", Q_tfidf, D_tfidf)

bert = BERT(V)
bert.load_state_dict(torch.load("bert.pt"))
bert.eval()
with torch.no_grad():
    D = vetores(bert, restos, tok)
    Q = vetores(bert, objetos, tok, T=32)
    mede("BERT, média", Q, D)
print(f"  cosseno médio entre atos: {(D @ D.T).mean():.3f}")
centro = D.mean(0)                  # tirar a direção comum
Dc = torch.nn.functional.normalize(D - centro, dim=-1)
Qc = torch.nn.functional.normalize(Q - centro, dim=-1)
mede("BERT, centrado", Qc, Dc)

_ = torch.manual_seed(0)
opt = torch.optim.AdamW(bert.parameters(), lr=1e-3)
bert.train()
inicio = time.time()
for passo in range(300):
    lote = torch.randint(0, len(treino), (32,))
    q = vetores(bert, [treino[i][0] for i in lote], tok, T=32)
    d = vetores(bert, [treino[i][1] for i in lote], tok)
    perda = infonce(q, d, tau=0.1)
    opt.zero_grad()
    perda.backward()
    opt.step()
    if (passo + 1) % 100 == 0:
        print(f"passo {passo + 1}  perda {perda.item():.3f}")
print(f"treino: {time.time() - inicio:.0f} s")
bert.eval()
torch.save(bert.state_dict(), "busca.pt")
with torch.no_grad():
    D = vetores(bert, restos, tok)
    Q = vetores(bert, objetos, tok, T=32)
    mede("BERT, contraste", Q, D)
print(f"  cosseno médio entre atos: {(D @ D.T).mean():.3f}")
