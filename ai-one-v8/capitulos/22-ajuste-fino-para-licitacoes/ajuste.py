import time

import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from lupa.ajuste import Classificador, preve, tensores, treina
from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos, gabarito, le

torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
corpus = {a["id"]: a for a in atos()}
verdade = gabarito()
# treino: os rotulados de 2026, menos os de palavras raras
rotulados = [r for r in le("rotulos.jsonl")
             if corpus[r["id"]]["data"] < "2027"
             and not verdade[r["id"]]["raro"]]
treino = [corpus[r["id"]]["texto"] for r in rotulados]
y = torch.tensor([int(r["relevante"]) for r in rotulados])
de_2027 = [a for a in corpus.values() if a["data"] >= "2027"]
teste = [a["texto"] for a in de_2027]
y_teste = torch.tensor([int(verdade[a["id"]]["relevante"])
                        for a in de_2027])
raros = torch.tensor([verdade[a["id"]]["raro"]
                      for a in de_2027])
print(f"treino: {len(treino)} atos, {y.sum()} relevantes")
print(f"teste: {len(teste)} atos, {y_teste.sum()} relevantes,"
      f" {raros.sum()} com palavras raras")
ids, vazio = tensores(treino, tok)
ids_t, vazio_t = tensores(teste, tok)


@torch.no_grad()
def medias(bert, ids, vazio):
    """A média dos estados de cada ato: um vetor de 128."""
    h = bert(ids, vazio)
    cheio = (~vazio).unsqueeze(-1).float()
    return ((h * cheio).sum(1) / cheio.sum(1)).numpy()


previsoes = {}
tfidf = TfidfVectorizer(sublinear_tf=True)
logistica = LogisticRegression(C=10, max_iter=1000)
logistica.fit(tfidf.fit_transform(treino), y)
previsoes["TF-IDF e logística"] = logistica.predict(
    tfidf.transform(teste))

for nome, pre in [("sonda, aleatório", False),
                  ("sonda, pré-treinado", True)]:
    torch.manual_seed(0)
    bert = BERT(V)
    if pre:
        bert.load_state_dict(torch.load("bert.pt"))
    bert.eval()
    sonda = LogisticRegression(C=100, max_iter=5000)
    sonda.fit(medias(bert, ids, vazio), y)
    x_teste = medias(bert, ids_t, vazio_t)
    previsoes[nome] = sonda.predict(x_teste)

for nome, pre in [("ajuste completo", True),
                  ("sem pré-treino", False)]:
    torch.manual_seed(0)
    bert = BERT(V)
    if pre:
        bert.load_state_dict(torch.load("bert.pt"))
    modelo = Classificador(bert)
    inicio = time.time()
    treina(modelo, ids, vazio, y, modelo.parameters(), lr=3e-4)
    print(f"{nome}: {time.time() - inicio:.0f} s")
    previsoes[nome] = preve(modelo, ids_t, vazio_t).numpy()
    if pre:
        torch.save(modelo.state_dict(), "relevancia.pt")

print()
for nome, p in previsoes.items():
    p = torch.tensor(p)
    vp = ((p == 1) & (y_teste == 1)).sum().item()
    fp = ((p == 1) & (y_teste == 0)).sum().item()
    fn = ((p == 0) & (y_teste == 1)).sum().item()
    achados = (p[raros] == 1).sum().item()
    print(f"{nome:19} VP {vp} FP {fp:2} FN {fn:2}"
          f"  F1 {2 * vp / (2 * vp + fp + fn):.3f}"
          f"  raros {achados}/{raros.sum()}")
torch.save({"previsoes": previsoes, "y": y_teste},
           "previsoes.pt")
