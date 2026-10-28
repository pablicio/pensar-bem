import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from lupa.autoatencao import Autoatencao

torch.manual_seed(0)
x = torch.randn(2, 6, 16)                  # 2 frases, 6 tokens
preenchido = torch.zeros(2, 6, dtype=torch.bool)
preenchido[1, 4:] = True                   # a 2ª tem 4 tokens

for causal in [False, True]:
    camada = Autoatencao(16, 8, causal=causal)
    saida = camada(x, preenchido)
    # a mesma conta pela função do PyTorch
    q, k, v = camada.W_q(x), camada.W_k(x), camada.W_v(x)
    permitido = ~preenchido[:, None, :]
    if causal:
        permitido = permitido & torch.ones(6, 6).tril().bool()
    ref = F.scaled_dot_product_attention(q, k, v,
                                         attn_mask=permitido)
    print(f"causal={causal}: saída {tuple(saida.shape)},",
          f"diferença {(saida - ref).abs().max():.1e}")
    print(camada.pesos[1].detach().numpy().round(2))

fig, eixos = plt.subplots(1, 2, figsize=(7, 3.2))
for eixo, causal in zip(eixos, [False, True]):
    torch.manual_seed(1)
    camada = Autoatencao(16, 8, causal=causal)
    camada(x[:1])
    eixo.imshow(camada.pesos[0].detach(), cmap="Greys",
                vmin=0, vmax=1)
    eixo.set_title("causal" if causal else "todos com todos")
    eixo.set_xlabel("chave (para quem olha)")
eixos[0].set_ylabel("consulta (quem olha)")
fig.tight_layout()
fig.savefig("mascaras.png", dpi=300)
