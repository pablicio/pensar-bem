import time

import torch
from torch.utils.flop_counter import FlopCounterMode

from lupa.corpus import prepara
from lupa.escolha import gulosa
from lupa.gpt import GPT
from lupa.kv import gera, passo

torch.set_num_threads(1)
tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()
ids = tok.codifica("<|fim|>EXTRATO DO CONTRATO Nº 012/2026\n")
x = torch.tensor([ids])

# 1. o mesmo resultado que o modelo completo
cache = [([], []) for _ in modelo.blocos]
for t, i in enumerate(ids):
    logits = passo(modelo, torch.tensor([i]), t, cache)
dif = (logits - modelo(x)[0, -1]).abs().max().item()
print(f"último token, cache contra o modelo todo: {dif:.1e}")

# 2. operações e tempo para escrever 100 tokens
def sem_cache():
    return modelo.gera(x, 100, gulosa)[0].tolist()


jeitos = {"sem cache": sem_cache,
          "com cache": lambda: gera(modelo, ids, 100)}
textos = {}
for nome, f in jeitos.items():
    with FlopCounterMode(display=False) as conta:
        textos[nome] = f()
    inicio = time.time()
    f()
    bilhoes = conta.get_total_flops() / 1e9
    print(f"{nome}: {bilhoes:.2f} bilhões de operações,"
          f" {time.time() - inicio:.2f} s")
iguais = textos["sem cache"] == textos["com cache"]
print("o mesmo texto:", iguais)

# 3. a memória do cache: K e V, T x d, em cada bloco
for nome, L, T, d in [("GPT pequeno", 4, 128, 128),
                      ("GPT-3", 96, 2048, 12288)]:
    numeros = 2 * L * T * d
    print(f"{nome}: 2 L T d = {numeros:.3g} números,"
          f" {numeros * 2 / 1e9:.3g} GB em 16 bits")
