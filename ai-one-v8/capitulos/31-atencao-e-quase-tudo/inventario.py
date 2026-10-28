from lupa.bert import BERT
from lupa.gpt import GPT
from lupa.vit import ViT

V, T, d, L = 2000, 128, 128, 4
bloco = 12 * d * d + 9 * d               # o capítulo 11


def conta(modelo):
    return sum(p.numel() for p in modelo.parameters())


modelos = [
    ("GPT, cap. 17", GPT(V),
     V * d + T * d + L * bloco + 2 * d),
    ("BERT, cap. 21", BERT(V),
     (V + 3) * d + L * bloco + 2 * d),
    ("ViT, cap. 27", ViT(),
     64 * 64 + 64 + 64 + 17 * 64 + 2 * (12 * 64 * 64 + 9 * 64)
     + 2 * 64 + 64 * 10 + 10),
]
print(f"{'modelo':14} {'contado':>9} {'fórmula':>9}")
for nome, modelo, formula in modelos:
    print(f"{nome:14} {conta(modelo):9} {formula:9}")
