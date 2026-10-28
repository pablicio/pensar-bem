import torch
from sklearn.feature_extraction.text import TfidfVectorizer

from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos, gabarito
from lupa.extrator import limpa
from lupa.vetores import vetores

tok, _, _ = prepara()
verdade = gabarito()
de_2027 = [a for a in atos() if a["data"] >= "2027"]
textos = [limpa(a["texto"]) for a in de_2027]
relevante = torch.tensor([verdade[a["id"]]["relevante"]
                          for a in de_2027])
raro = torch.tensor([verdade[a["id"]]["raro"]
                     for a in de_2027])
R = relevante.sum().item()
pergunta = "Pavimentação e recapeamento de ruas e avenidas"
print(f"{len(textos)} atos, {R} obras viárias,"
      f" {raro.sum()} com palavras raras")

tfidf = TfidfVectorizer(sublinear_tf=True).fit(textos)
notas_tfidf = torch.tensor(
    (tfidf.transform(textos) @ tfidf.transform([pergunta]).T)
    .toarray()[:, 0])
bert = BERT(len(tok.vocab))
bert.load_state_dict(torch.load("busca.pt"))
bert.eval()
with torch.no_grad():
    D = vetores(bert, textos, tok)
    q = vetores(bert, [pergunta], tok, T=32)[0]



def posicoes(notas):
    """A posição de cada ato no ranking (0 = o primeiro)."""
    return notas.argsort(descending=True).argsort().float()


# fusão pelas posições: 1 / (60 + posição) somado nas duas
fusao = (1 / (60 + posicoes(notas_tfidf))
         + 1 / (60 + posicoes(D @ q)))
for nome, notas in [("TF-IDF", notas_tfidf),
                    ("BERT, contraste", D @ q),
                    ("fusão", fusao)]:
    ordem = notas.argsort(descending=True)
    rel, rar = relevante[ordem], raro[ordem]
    primeiro_raro = rar.float().argmax().item() + 1
    print(f"{nome}: top 10 {rel[:10].sum()},"
          f" top {R} {rel[:R].sum()} ({rar[:R].sum()} raras),"
          f" 1ª rara {primeiro_raro}º")
    if nome == "BERT, contraste":
        for i in ordem[rar[:R].nonzero()[:3, 0]]:
            t = textos[i]
            print("  ", t[t.find("Objeto"):][:58])
